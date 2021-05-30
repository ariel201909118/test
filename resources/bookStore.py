from flask import Response, request
from database.models import books, User
from flask_restful import Resource
from flask_jwt_extended.view_decorators import jwt_required
import datetime
from flask_jwt_extended import create_access_token
import json


class BooksAPI(Resource):
    
    @jwt_required
    def get(self):
        books_collection = books.objects().to_json()
        collection = json.dumps(json.loads(books_collection), indent=4)
        return Response(collection, mimetype="application/json", status=200)
        
    @jwt_required
    def post(self):
        body = request.get_json()
        book = books(**body).save()
        identification = book.book_id
        return {'id' : int(identification)}, 200

class SingleBookAPI(Resource):
    
    @jwt_required
    def get(self, id):
        book = books.objects.get(book_id=id).to_json()
        return Response(book, mimetype="application/json", status=200)
    
    @jwt_required
    def put(self, id):
        body = request.get_json()
        books.objects.get(book_id=id).update(**body)
        return 'Book Updated', 200
    
    @jwt_required    
    def delete(self, id):
        books.objects.get(book_id=id).delete()
        return Response('Book Deleted Successfully', mimetype="application/json", status=200)

class RegisterAPI(Resource):
    
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        user.save()
        id = user.id 
        return {'id': str(id)}, 200

class LoginAPI(Resource):
    
    def post(self):
        body = request.get_json()
        user = User.objects.get(email = body.get('email'))
        authorized = user.check_password(body.get('password'))

        if not authorized:
            return {'Error': 'Invalid Credentials'}, 401
        
        expiry = datetime.timedelta(days=1)
        access_token = create_access_token(identity=str(user.id), expires_delta=expiry)
        return {'token': access_token}, 200