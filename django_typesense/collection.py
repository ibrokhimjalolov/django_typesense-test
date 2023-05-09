from typesense import Client
from dj_typesense.typesense_s import TYPESENSE_CLIENT_SETTINGS

# All registered document classes
registry = dict()



class Collection:
    __collection_name: str
    __document_types: list
    
    __fields: list


    def __init__(self, collection_name, document_types: list) -> None:
        self.__collection_name = collection_name
        self.__document_types = document_types
        self.__fields = document_types[0].get_fields()
        
        from . import signals
        registry[self.get_collection_name()] = self
        signals.document_connect_signals(self)

    def get_fields(self):
        return self.__fields
    
    def get_collection_schema(self):
        schema = {
            'name': self.get_collection_name(),
            'fields': self.get_fields_schema(),
        }
        return schema
    
    def get_fields_schema(self):
        """
        Typesense schema ni qaytaradi
        :return:
        """
        schema = list()
        fields = self.get_fields()
        for field in fields:
            schema.append(field.to_schema())
        return schema
    
    def get_document_types(self):
        return self.__document_types
    
    def get_serialized_data(self, instance) -> dict:
        for document in self.get_document_types():
            if isinstance(instance, document.model):
                data = document.serialize(instance)
                break
        else:
            raise ValueError(f'{instance} is not registered in TypesenseDocument._registry')
        
        for field in self.get_fields():
            if field.name not in data:
                data[field.name] = field.to_typesense_value(None)
        
        return data
    
    def get_client(self) -> Client:
        return Client(TYPESENSE_CLIENT_SETTINGS)

    def get_collection_name(self):
        return self.__collection_name

    def get_collection(self):
        client = self.get_client()
        collection_name = self.get_collection_name()
        return client.collections[collection_name]

    def create_collection(self):
        """Create collection in typesense"""
        schema = self.get_collection_schema()
        print(schema)
        client = self.get_client()
        return client.collections.create(schema)

    def delete_collection(self):
        """Delete collection in typesense"""
        collection = self.get_collection()
        return collection.delete()

    def insert_document(self, instance):
        """
        Insert document to typesense
        :param instance:
        :return:
        """
        collection = self.get_collection()
        serialized_data = self.get_serialized_data(instance)
        return collection.documents.create(serialized_data)

    def insert_document_bulk(self, instances, batch_size=1000):
        """
        Bulk insert document to typesense
        :param instances:
        :param batch_size:
        :return:
        """
        
        collection = self.get_collection()
        
        return collection.documents.import_(
            [ self.get_serialized_data(instance) for instance in instances], 
            batch_size=batch_size
        )

    def update_document(self, instance):
        """
        Update document in typesense
        :param instance:
        :return:
        """
        collection = self.get_collection()
        return collection.documents.update(self.get_serialized_data(instance))

    def delete_document(self, instance):
        """
        Delete document from typesense
        :param instance:
        :return:
        """
        collection = self.get_collection()
        serialized_data = self.get_serialized_data(instance)
        return collection.documents[serialized_data["id"]].delete()

    def search(self, schema):
        """
        Search in collection
        :param schema:
        :return:
        """
        collection = self.get_collection()
        return collection.documents.search(schema)

    def __repr__(self):
        return f'<Collection {self.get_collection_name()}>'
