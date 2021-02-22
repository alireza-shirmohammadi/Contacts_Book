# This is app.py, this is the main file called.
from myproject import app
from flask import render_template

from flask import (
    Blueprint,
    jsonify,
    request,
)

from marshmallow import ValidationError
from myproject.models import Contacts
from myproject import db
from flask_restful import Resource
from myproject.contacts.serializers import ContactsSerializers,CreateContactsSerializers
from myproject import api

api_blueprint=Blueprint('/api',__name__)
class ContactDetailApi(Resource):

    def get(self,name):
        print(name)
        query = Contacts.query.filter_by(name=name).first()
        serializer=ContactsSerializers().dump(query)
        return jsonify(serializer)




    def put(self,name):
        try:
            query=Contacts.query.filter_by(name=name).first()
            serializer=ContactsSerializers().load(request.json)
            query1=Contacts.query.filter_by(name=name).update(serializer)
            db.session.commit()
            result=ContactsSerializers().dump(query)
            return jsonify(result)
        except ValidationError as err:
            return {"message": 'something went wrong'}, 400




    def delete(self,name):
        query = Contacts.query.filter_by(name=name).first()
        if query is not None:
            db.session.delete(query)
            db.session.commit()
            return {'message':f'contact {query.name} is successfully deleted'},202
        return {'message':'contact not found'},404


class CreateContactAPI(Resource):

    def post(self):
        try:

            serializer = CreateContactsSerializers().load(request.json)
            new_con= Contacts(name=serializer['name'],phone=serializer['phone'])
            db.session.add(new_con)
            db.session.commit()
            return {'message':f'Contact with name {new_con.name} successfully created'},201
        except ValidationError as err:
            return {"message" : err.messages},400

class ContactsListAPI(Resource):

    def get(self):
        query = Contacts.query.all()
        serializer = ContactsSerializers(many=True).dump(query)
        return jsonify(serializer)




api.add_resource(ContactDetailApi,'/api/contact/<string:name>')
api.add_resource(CreateContactAPI,'/api/create')
api.add_resource(ContactsListAPI,'/api/list')


if __name__ == "__main__":
    app.run(debug=True)
