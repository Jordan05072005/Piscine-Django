from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra):
        user = self.model(username=username, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra):
        extra.setdefault("is_staff", True)
        extra.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra)




    # def authenticate(self, username, password):
    #     try:
    #         user = self.get(username=username)
    #     except self.model.DoesNotExist:
    #         return None
    #     if check_password(password, user.password):
    #         return user
    #     return None


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    reputation = models.IntegerField(default=0)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    upvotes = models.ManyToManyField(User, related_name='upvotes')
    downvotes = models.ManyToManyField(User, related_name='downvotes')

    class Meta:
        permissions = (
            ("can_downvote", "Can Downvote Tip"),
        )



