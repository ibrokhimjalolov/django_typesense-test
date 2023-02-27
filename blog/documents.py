from blog.models import Post
from django_typesense.document import TypesenseDocument, register_doc

from django_typesense.serializer import TypesenseDocumentSerializer


# typesense field types
STRING = "string"
INT32 = "int32"
BOOL = "bool"
STRING_ARRAY = "string[]"
INT32_ARRAY = "int32[]"
BOOL_ARRAY = "bool[]"
# end typesense field types


class PostDocumentSerializer(TypesenseDocumentSerializer):

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "body",
            "number"
        ]

    @classmethod
    def get_document_fields(cls) -> list:
        return [
            {"name": "id", "type": STRING},
            {"name": "title", "type": STRING},
            {"name": "body", "type": STRING, "facet": True},
            {"name": "number", "type": INT32, "facet": True, "sortable": True},
        ]


@register_doc
class PostDocument(TypesenseDocument):
    DOCUMENT_NAME = "post_document"
    typesense_serializer_class = PostDocumentSerializer
    dj_model_cls = Post
