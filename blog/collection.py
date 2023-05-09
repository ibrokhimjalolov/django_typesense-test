from django_typesense._documents import Document
from django_typesense.collection import Collection
from django_typesense.fields import CharField
from .models import Post


class PostDocument(Document):
    model = Post
    fields = [
        CharField(name='id', default=''),
        CharField(name='title', default=''),
    ]
