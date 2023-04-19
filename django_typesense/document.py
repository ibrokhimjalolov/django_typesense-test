from typesense import Client

from .client import get_typesense_client


# All registered document classes
registry = dict()


def register_doc(typesense_document_cls):
    """This decorator register document class in registry"""
    from .signals import document_connect_signals
    typesense_document_cls.__new__(typesense_document_cls)
    registry[typesense_document_cls.dj_model_cls] = typesense_document_cls
    document_connect_signals(typesense_document_cls)
    return typesense_document_cls


class TypesenseDocument:

    DOCUMENT_NAME = None
    primary_key = 'id'
    typesense_serializer_class = None
    _client: Client = get_typesense_client()
    _collection = None
    dj_model_cls = None

    def __new__(cls, *args, **kwargs):
        if cls.DOCUMENT_NAME is None:
            raise ValueError('COLLECTION_NAME must be set')
        cls._collection = cls._client.collections[cls.DOCUMENT_NAME]
        cls = super().__new__(cls)
        return cls

    @classmethod
    def get_fields(cls):
        sr_fields = cls.typesense_serializer_class.get_document_fields()
        if cls.primary_key not in [field['name'] for field in sr_fields]:
            raise ValueError('primary_key must be in typesense_serializer_class.Meta.fields')
        return sr_fields

    @classmethod
    def create_collection(cls):
        """Create collection in typesense"""
        dj_model_collection_scheme = {
            'name': cls.DOCUMENT_NAME,
            'fields': cls.get_fields(),
        }
        return cls._client.collections.create(dj_model_collection_scheme)

    @classmethod
    def delete_collection(cls):
        """Delete collection in typesense"""
        return cls._client.collections[cls.DOCUMENT_NAME].delete()

    @classmethod
    def _model_instance_to_typesense(cls, instance):
        """
        Convert model instance to typesense document
        """
        return cls.typesense_serializer_class(instance=instance).data

    @classmethod
    def insert_document(cls, instance):
        """
        Insert document to typesense
        :param instance:
        :return:
        """
        return cls._collection.documents.create(cls._model_instance_to_typesense(instance))

    @classmethod
    def insert_document_bulk(cls, instances, batch_size=1000):
        """
        Bulk insert document to typesense
        :param instances:
        :param batch_size:
        :return:
        """
        data = [cls._model_instance_to_typesense(instance) for instance in instances]
        return cls._collection.documents.import_(data, batch_size=batch_size)

    @classmethod
    def update_document(cls, instance):
        """
        Update document in typesense
        :param instance:
        :return:
        """
        return cls._collection.documents.update(cls._model_instance_to_typesense(instance))

    @classmethod
    def delete_document(cls, instance):
        """
        Delete document from typesense
        :param instance:
        :return:
        """
        primary_key_value = getattr(instance, cls.primary_key)
        return cls._collection.documents[primary_key_value].delete()

    @classmethod
    def get_model_queryset(cls):
        """
        Get model queryset
        :return:
        """
        return cls.dj_model_cls.objects.all()

    @classmethod
    def get_searchable_fields(cls):
        """
        Get searchable fields, id field is excluded
        :return:
        """
        return [field['name'] for field in cls.get_fields() if field['name'] != 'id']

    @classmethod
    def search(cls, schema):
        """
        Search in collection
        :param schema:
        :return:
        """
        return cls._collection.documents.search(schema)

    def __repr__(self):
        return f'<Collection {self.DOCUMENT_NAME}>'
