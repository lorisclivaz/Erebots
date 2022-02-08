import datetime

from mongoengine import Document, StringField, DateTimeField, IntField, EmbeddedDocument, ReferenceField, ListField, \
    EmbeddedDocumentListField, BooleanField, EmbeddedDocumentField

from common.chat.language_enum import Language
from common.database.persuation.field_enums import ActionTypeField, QueryTypeField


class CacheData(Document):
    """Model class for cache data"""

    id = StringField(primary_key=True)
    timestamp = DateTimeField(required=True, default=datetime.datetime.now())
    cache_over_number = IntField(required=True)
    cache_data = StringField(required=True)

    meta = {
        'ordering': ['-timestamp']
    }


# TODO 04/06/2020: This class should be used to refactor suggestion events in Profiles chatBot
class AbstractSuggestionEvent(EmbeddedDocument):
    """Abstract model class to represent all events which carry a suggestion to be evaluated by the user"""

    datetime = DateTimeField(required=True)
    suggestion_message_id = StringField()
    suggestion_usefulness = StringField()

    meta = {
        'abstract': True,
        'ordering': ['-datetime'],
    }


# TODO 04/06/2020: this class should be used to localize Profiles Bot
class AbstractLocalizedObject(Document):
    """Abstract model class to represent all objects with a localizable text"""

    text_en = StringField(required=True)
    text_it = StringField()
    text_fr = StringField()
    text_de = StringField()

    meta = {
        'abstract': True,
        'ordering': ['text_en'],
    }


class AbstractLocalizedEmbeddedObject(EmbeddedDocument):
    """Abstract model class to represent all objects with a localizable text"""

    text_en = StringField(required=True)
    text_it = StringField()
    text_fr = StringField()
    text_de = StringField()


class BasicUser(Document):
    """Abstract model class to represent a basic user"""

    first_name = StringField()
    last_name = StringField()
    language = StringField(choices=Language.values())
    last_interaction = DateTimeField()

    meta = {
        'abstract': True,
        'ordering': ['-last_interaction']
    }


class Strategy(Document):
    """Model class to represent a strategy"""

    name = StringField()
    description = StringField()
    nodes = ListField(ReferenceField('Node'))


class KeyboardTransition(EmbeddedDocument):
    text = EmbeddedDocumentField(AbstractLocalizedEmbeddedObject)
    transition = ReferenceField('Node')


class Action(EmbeddedDocument):
    """Model class to represent a node action"""

    type = StringField(choices=ActionTypeField.values())
    trigger = DateTimeField()
    text = EmbeddedDocumentField(AbstractLocalizedEmbeddedObject)
    keyboard = EmbeddedDocumentListField(AbstractLocalizedEmbeddedObject, default=list)
    transition = ReferenceField('Node')
    delay = IntField()
    query = StringField(choices=QueryTypeField.values())
    threshold = IntField()
    greater_than = BooleanField()
    keyboard_transitions = EmbeddedDocumentListField(KeyboardTransition, default=list)


class Node(Document):
    """Model class to represent a strategy node"""

    name = StringField()
    description = StringField()
    parent = ReferenceField('self')
    actions = EmbeddedDocumentListField('Action', default=list)
