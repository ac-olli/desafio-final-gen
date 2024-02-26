from flask_restx import fields
from datetime import datetime
from .extensions import api

user_input_model = api.model("UserInput", {
    "name": fields.String,
    "email": fields.String,
    "foto": fields.String
})

tema_input_model = api.model("TemaInput", {
    "descricao": fields.String
})

user_model = api.model("User", {
    "id": fields.Integer,
    "name": fields.String,
    "email": fields.String,
    "foto": fields.String,
    "postagens": fields.List(fields.String)  
})

postagem_model = api.model("Postagem", {
    "id": fields.Integer,
    "titulo": fields.String,
    "texto": fields.String,
    "data": fields.DateTime(dt_format='iso8601'),
    "usuario_id": fields.Nested(user_model),
    "tema_id": fields.Integer
})

tema_model = api.model("Tema", {
    "id": fields.Integer,
    "descricao": fields.String,
    "postagens": fields.List(fields.Nested(postagem_model))
})

postagem_model['tema_id'] = fields.Nested(tema_model)

postagem_input_model = api.model("PostagemInput", {
    "titulo": fields.String,
    "texto": fields.String,
    "data": fields.DateTime(dt_format='iso8601'),
    "usuario_id": fields.Integer,
    "tema_id": fields.Integer
})





