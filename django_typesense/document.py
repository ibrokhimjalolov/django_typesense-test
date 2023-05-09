from django_typesense.fields import BaseField
from typing import List
from django.db.models import Model


class Document:
    """
    Document bu model dan typesense collection yaratish imkonini beradi
    """
    model: Model
    fields: List[BaseField]

    @classmethod
    def get_fields(cls) -> List[BaseField]:
        """
        Typesense schema ni qaytaradi
        :return:
        """
        return cls.fields

    @classmethod
    def get_fields_schema(cls):
        """
        Typesense schema ni qaytaradi
        :return:
        """
        schema = list()
        fields = cls.get_fields()
        for field in fields:
            schema.append(field.get_schema())
        return schema

    @classmethod
    def serialize(cls, instance) -> dict:
        data = dict()
        for field in cls.get_fields():
            getter_method = getattr(instance, f'get_{field.name}_value', None)
            if getter_method:
                value = getter_method(instance)
            else:
                value = getattr(instance, field.name)
            data[field.name] = field.to_typesense_value(value)
        return data
