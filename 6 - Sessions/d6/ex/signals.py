from django.dispatch import receiver
from .models import User
from django.contrib.auth.models import Permission
from django.db.models.signals import pre_save, pre_delete
from .models import Tip

@receiver(pre_save, sender=User)
def on_reputation_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    old = sender.objects.filter(pk=instance.pk).values_list("reputation", flat=True).first()
    if old is None or old == instance.reputation:
        return

    downVotePerm = Permission.objects.get(codename="can_downvote", content_type__app_label="ex")
    deleteTipsPerm = Permission.objects.get(codename="delete_tip", content_type__app_label="ex")


    if instance.reputation >= 15:
        instance.user_permissions.add(downVotePerm)
    else:
        instance.user_permissions.remove(downVotePerm)
    if instance.reputation >= 30:
        instance.user_permissions.add(deleteTipsPerm)
    else:
        instance.user_permissions.remove(deleteTipsPerm)


@receiver(pre_delete, sender=Tip)
def on_tip_delete(sender, instance, **kwargs):
    author = instance.author
    author.reputation -= instance.upvotes.count() * 5
    author.reputation += instance.downvotes.count() * 2
    author.save()
