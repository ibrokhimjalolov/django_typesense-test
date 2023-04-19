import uuid

from django.core.management.base import BaseCommand

from blog.models import Post


class Command(BaseCommand):
    help = "Fill DB with fake data"

    def handle(self, *args, **options):
        posts_list = []
        for i in range(100000):
            posts_list.append(Post(title=f"Post {i}", body=f"Body {uuid.uuid4()} uic {i}", number=i))
        Post.objects.bulk_create(posts_list, batch_size=5000)
