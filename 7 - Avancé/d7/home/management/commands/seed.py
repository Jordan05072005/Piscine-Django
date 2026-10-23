from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from articles.models import Article, UserFavouriteArticle


USERS = [
    {"username": "jguaglio", "password": 'password'},
    {"username": "tbonnet", "password": 'password'},
    {"username": "nferrer", "password": 'password'},
]

ARTICLES = [
    {
        "author": "jguaglio",
        "title": "Surviving the 42 Perpignan piscine",
        "synopsis": "Four intense weeks, C from day one and not a single teacher: a first-hand account of the piscine and tips to make it to the end.",
        "content": (
            "The piscine is four weeks of C, shell, and short nights. "
            "The first piece of advice: don't stay alone. At 42, you learn through peer learning, "
            "and the person at the next cluster often knows more than any tutorial.\n\n"
            "Second piece of advice: submit exercises, even imperfect ones. The Moulinette forgives nothing, "
            "but every failure teaches you exactly what was missing.\n\n"
            "Finally, sleep. A rested brain fixes a segfault in ten minutes; "
            "an exhausted one spends the whole night on it."
        ),
    },
    {
        "author": "tbonnet",
        "title": "The Norminette explained to newcomers",
        "synopsis": "Functions of 25 lines max, no for loops, declarations at the top of the block: why the Norm exists and how to tame it without losing your mind.",
        "content": (
            "42's Norm enforces a strict style: short functions, five functions per file, "
            "no for loops, variables declared at the top of the function.\n\n"
            "At first, it feels arbitrary. Then you realize it forces you to break your code "
            "into small, readable functions, and that everyone can read everyone else's code with ease.\n\n"
            "Tip: run the Norminette before every push, not the night before the evaluation."
        ),
    },
    {
        "author": "nferrer",
        "title": "Coding at the foot of the Castillet",
        "synopsis": "Between the Catalan sun, the sea twenty minutes away, and the Pyrenees on the horizon, studying code in Perpignan has a charm few campuses can offer.",
        "content": (
            "Perpignan isn't the first city you'd think of for learning to code, "
            "and yet. The campus attracts people from all over the Occitanie region and beyond.\n\n"
            "After a debugging session, a walk to the Castillet or a weekend in Collioure "
            "helps clear your head.\n\n"
            "Here, the cost of living is lower than in big cities, "
            "which leaves more time and energy to focus on the curriculum."
        ),
    },
    {
        "author": "jguaglio",
        "title": "Peer evaluations: a how-to guide",
        "synopsis": "Correcting and being corrected is part of the curriculum. How to prepare for a defense, ask the right questions, and give genuinely useful feedback.",
        "content": (
            "At 42, every project is evaluated by other students. This system demands rigor "
            "on both sides.\n\n"
            "When you're being evaluated: know every line of your code and prepare your tests. "
            "When you're evaluating: be demanding but kind, and always explain why "
            "something is wrong.\n\n"
            "A good evaluation is often where you learn the most."
        ),
    },
    {
        "author": "tbonnet",
        "title": "From Libft to Django: my journey through the common core",
        "synopsis": "Libft, get_next_line, ft_printf, then the specialized piscines: the story of a progression, from the first functions in C to web applications.",
        "content": (
            "It all starts with Libft, your own library of C functions. "
            "You then reuse it in almost every project of the common core.\n\n"
            "Next come get_next_line, ft_printf, then the network and graphics projects. "
            "Each step adds a building block: memory, processes, algorithms.\n\n"
            "Reaching the Django piscine after that means discovering just how much time a framework "
            "saves, while still understanding what it does under the hood."
        ),
    },
]


class Command(BaseCommand):
    help = "Creates 3 users and 5 demo articles on the theme of 42 Perpignan."

    @transaction.atomic
    def handle(self, *args, **options):
        users = {}
        for data in USERS:
            user, created = User.objects.get_or_create(username=data["username"])
            if created:
                user.set_password(data["password"])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"User created: {user.username}"))
            else:
                self.stdout.write(f"User already exists: {user.username}")
            users[user.username] = user

        articles = {}
        for data in ARTICLES:
            article, created = Article.objects.get_or_create(
                title=data["title"],
                defaults={
                    "author": users[data["author"]],
                    "synopsis": data["synopsis"],
                    "content": data["content"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Article created: {article.title}"))
            else:
                self.stdout.write(f"Article already exists: {article.title}")
            articles[article.title] = article


        UserFavouriteArticle.objects.get_or_create(
            user=users["jguaglio"],
            article=articles["From Libft to Django: my journey through the common core"],
        )
        UserFavouriteArticle.objects.get_or_create(
            user=users["jguaglio"],
            article=articles["The Norminette explained to newcomers"],
        )
        UserFavouriteArticle.objects.get_or_create(
            user=users["jguaglio"],
            article=articles["Peer evaluations: a how-to guide"],
        )

        self.stdout.write(self.style.SUCCESS(
            f"Done. User password: password"
        ))
