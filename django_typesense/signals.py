from django.db.models.signals import post_save, post_delete
from django_typesense.collection import registry

signal_registred_models = set()


def ts_sync_post_save(sender, instance, created, **kwargs):
    """Sync post save signal"""
    for collection in registry.values():
        if sender in [document.model for document in collection.get_document_types()]:
            if created:
                print('inserting')
                collection.insert_document(instance)
            else:
                print('updating')
                collection.update_document(instance)


def ts_sync_post_delete(sender, instance, **kwargs):
    """Sync post delete signal"""
    for collection in registry.values():
        if sender in [document.model for document in collection.get_document_types()]:
            collection.delete_document(instance)


def document_connect_signals(collection):
    for document in collection.get_document_types():
        if document.model not in signal_registred_models:
            post_save.connect(ts_sync_post_save, sender=document.model)
            post_delete.connect(ts_sync_post_delete, sender=document.model)
            signal_registred_models.add(document.model)
