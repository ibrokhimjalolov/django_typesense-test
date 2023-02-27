from .document import registry
from django.db.models.signals import post_save, post_delete


def ts_sync_post_save(sender, instance, created, **kwargs):
    """Sync post save signal"""
    document_cls = registry.get(sender)
    if document_cls is not None:
        if created:
            document_cls.insert_document(instance)
        else:
            document_cls.update_document(instance)
    else:
        raise ValueError(f'{sender} is not registered in TypesenseDocument._registry')


def ts_sync_post_delete(sender, instance, **kwargs):
    """Sync post delete signal"""
    document_cls = registry.get(sender)
    if document_cls is not None:
        document_cls.delete_document(instance)
    else:
        raise ValueError(f'{sender} is not registered in TypesenseDocument._registry')


def document_connect_signals(document_cls):
    post_save.connect(ts_sync_post_save, sender=document_cls.dj_model_cls)
    post_delete.connect(ts_sync_post_delete, sender=document_cls.dj_model_cls)
