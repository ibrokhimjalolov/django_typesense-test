from rest_framework import serializers


class TypesenseDocumentSerializer(serializers.ModelSerializer):
    """Typesense Documentga Model instance saqlash strukturasi"""
    id = serializers.CharField(read_only=True)  # Typesense document id must be string

    @classmethod
    def get_document_fields(cls) -> list:
        """
        Returns a list of fields that should be indexed in the document.
        :return: example
        [{"name": "id", "type": "int32"}, {"name": "title", "type": "string"}]
        """
        raise NotImplementedError("get_document_fields() must be implemented")


class DocumentTypesenseSuggestSerializer(serializers.Serializer):

    class DocumentTypesenseSuggestChildSerializer(serializers.Serializer):
        id = serializers.CharField()
        text = serializers.CharField()
    results = serializers.ListField(child=DocumentTypesenseSuggestChildSerializer())
