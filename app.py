from flask import Flask 
from flask_restful import Api
from database.db import initialize_db
from resources.routes import initialize_route
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

app = Flask(__name__)
api = Api(app)

DB_ATLAS_URI = "mongodb://Ariel:ZeULZmOSuoqcFbli@cluster0-shard-00-00.spkl4.mongodb.net:27017,cluster0-shard-00-01.spkl4.mongodb.net:27017,cluster0-shard-00-02.spkl4.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-lkuazr-shard-0&authSource=admin&retryWrites=true&w=majority"
app.config["MONGODB_HOST"] = DB_ATLAS_URI
app.config["SECRET_KEY"] = 'mcit-cst-authorization'

initialize_db(app)
initialize_route(api)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

if __name__ =="__main__":
  app.run(debug='True', port=80)