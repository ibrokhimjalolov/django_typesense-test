from django_typesense.document import Document
from django_typesense.collection import Collection
from django_typesense.fields import CharField
from .models import Post


STRING = "string"
INT32 = "int32"
BOOL = "bool"
STRING_ARRAY = "string[]"
INT32_ARRAY = "int32[]"
BOOL_ARRAY = "bool[]"

class PostDocument(Document):
    model = Post
    fields = [
        CharField(name='id', default='', type=STRING),
        CharField(name='title', default='', type=STRING, index=True),
    ]


# typesense field types

# end typesense field types


PostCollection = Collection(
    collection_name="posts",
    document_types=[PostDocument],
)
