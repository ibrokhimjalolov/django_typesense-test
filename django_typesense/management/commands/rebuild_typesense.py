import datetime

from django.core.management.base import BaseCommand
from ...document import registry


class Command(BaseCommand):
    help = "Rebuilds Typesense documents"

    def log(self, *messages, sep=' '):
        message = sep.join([str(m) for m in messages])
        self.stdout.write(str(datetime.datetime.now()) + " | " + self.style.SUCCESS(message))

    def handle(self, *args, **options):
        collections = registry.values()
        for collection_class in collections:
            try:
                self.log(collection_class, "Deleting document...")
                collection_class.delete_collection()
            except Exception as e:
                self.log(e)
            self.log(collection_class, "Creating document...")
            collection_class.create_collection()
            self.log(f"Indexing {collection_class.get_model_queryset().count()} items...")
            collection_class.insert_document_bulk(collection_class.get_model_queryset())
            self.log(collection_class, "Done!")
            self.log("=" * 20)
