import datetime

from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = "Rebuilds Typesense documents"

    def log(self, *messages, sep=' '):
        message = sep.join([str(m) for m in messages])
        self.stdout.write(str(datetime.datetime.now()) + " | " + self.style.SUCCESS(message))

    def handle(self, *args, **options):
        from ...collection import registry
        for collection_name, collection in registry.items():
            try:
                self.log(collection, "Deleting document...")
                collection.delete_collection()
            except Exception as e:
                self.log(e)
            self.log(collection, "Creating document...")
            collection.create_collection()
            for document in collection.get_document_types():
                instances = document.model._default_manager.all()
                collection.insert_document_bulk(instances)
                self.log(collection, "Done!")
            self.log("=" * 20)
