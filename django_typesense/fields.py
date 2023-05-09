from abc import ABC, abstractmethod


class BaseField(ABC):
    name: str
    type: str
    facet: bool
    index: bool
    default: str
    
    def __init__(self, name=None, type=None, facet=False, index=False, default=None) -> None:
        self.name = name
        self.type = type
        self.facet = facet
        self.index = index
        self.default = default
    
    
    def to_typesense_value(self, value):
        print("to_typesense_value", value)
        return str(value)
    
    
    def to_schema(self):
        """
        Typesense schema ni qaytaradi
        :return:
        """
        
        return {
            "name": self.name,
            "type": self.type,
            "facet": self.facet,
            "index": self.index,
            "default": self.default,
        }



class CharField(BaseField):
    

    def to_typesense_value(self, value):
        return str(value)
