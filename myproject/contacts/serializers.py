
from marshmallow import Schema, fields , validate



class ContactsSerializers(Schema):

    name = fields.String()
    phone = fields.Integer()

class CreateContactsSerializers(Schema):

    name = fields.String(required=True)
    phone = fields.Integer(required=True)