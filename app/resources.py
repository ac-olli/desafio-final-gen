from flask_restx import Resource, Namespace, abort

from .extensions import db
from .models import *
from .api_models import *

ns = Namespace("api")
    
@ns.route("/user")
class UserListApi(Resource):
    @ns.marshal_list_with(user_model)
    def get(self):
        return User.query.all()
    
    @ns.expect(user_input_model)
    @ns.marshal_with(user_model)
    def post(self):
        print(ns.payload)
        user = User(name=ns.payload["name"], email=ns.payload["email"], foto=ns.payload["foto"])
        db.session.add(user)
        db.session.commit()
        return user, 201
    
@ns.route("/user/<int:id>")
class UserApi(Resource):
    @ns.marshal_with(user_model)
    def get(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message="Usuario não encontrado")
        return user
    
    @ns.expect(user_input_model)
    @ns.marshal_with(user_model)
    def put(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message="Usuario não encontrado")
        user.name = ns.payload["name"]
        user.email = ns.payload["email"]
        user.foto = ns.payload["foto"]
        db.session.commit()
        return user

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            abort(404, message="Usuario não encontrado")
        db.session.delete(user)
        db.session.commit()
        return "Usuario deletado", 204

@ns.route("/postagem")
class PostagemListApi(Resource):
    @ns.marshal_list_with(postagem_model)
    def get(self):
        postagens = Postagem.query.all()
        formatted_postagens = []
        for post in postagens:
            usuario = User.query.get(post.usuario_id)
            tema = Tema.query.get(post.tema_id)
            formatted_postagem = {
                "id": post.id,
                "titulo": post.titulo,
                "texto": post.texto,
                "data": post.data,
                "usuario_id": {
                    "id": usuario.id,
                    "name": usuario.name,
                    "email": usuario.email,
                    "foto": usuario.foto
                },
                "tema_id": {
                    "id": tema.id,
                    "descricao": tema.descricao
                }
            }
            formatted_postagens.append(formatted_postagem)

        return formatted_postagens 
    
    @ns.expect(postagem_input_model)
    @ns.marshal_with(postagem_model)
    def post(self):
        data = datetime.strptime(ns.payload["data"], '%Y-%m-%dT%H:%M:%S.%fZ')
        usuario = User.query.get(ns.payload["usuario_id"])
        tema = Tema.query.get(ns.payload["tema_id"])
        postagem = Postagem(titulo=ns.payload["titulo"], texto=ns.payload["texto"], data=data, usuario=usuario, tema=tema)

        db.session.add(postagem)
        db.session.commit()
        formatted_postagem = {
                "id": postagem.id,
                "titulo": postagem.titulo,
                "texto": postagem.texto,
                "data": postagem.data,
                "usuario_id": {
                    "id": usuario.id,
                    "name": usuario.name,
                    "email": usuario.email,
                    "foto": usuario.foto
                },
                "tema_id": {
                    "id": tema.id,
                    "descricao": tema.descricao
                }
            }    

        return formatted_postagem

    
@ns.route("/postagem/<int:id>")
class PostagemApi(Resource):
    @ns.marshal_with(postagem_model)
    def get(self, id):
        postagem = Postagem.query.get(id)
        usuario = User.query.get(postagem.usuario_id)
        tema = Tema.query.get(postagem.tema_id)
        if not postagem:
            abort(404, message="Postagem não encontrada")

        formatted_postagem = {
                "id": postagem.id,
                "titulo": postagem.titulo,
                "texto": postagem.texto,
                "data": postagem.data,
                "usuario_id": {
                    "id": usuario.id,
                    "name": usuario.name,
                    "email": usuario.email,
                    "foto": usuario.foto
                },
                "tema_id": {
                    "id": tema.id,
                    "descricao": tema.descricao
                }
            }    

        return formatted_postagem

    @ns.expect(postagem_put_input)
    @ns.marshal_with(postagem_model)
    def put(self, id):
        postagem = Postagem.query.get(id)
        
        if not postagem:
            abort(404, message="Postagem não encontrada")
        postagem.titulo = ns.payload["titulo"]
        postagem.texto = ns.payload["texto"]
        postagem.tema_id = ns.payload["tema_id"]
        db.session.commit()

        usuario = User.query.get(postagem.usuario_id)
        tema = Tema.query.get(postagem.tema_id)
        formatted_postagem = {
                "id": postagem.id,
                "titulo": postagem.titulo,
                "texto": postagem.texto,
                "data": postagem.data,
                "usuario_id": {
                    "id": usuario.id,
                    "name": usuario.name,
                    "email": usuario.email,
                    "foto": usuario.foto
                },
                "tema_id": {
                    "id": tema.id,
                    "descricao": tema.descricao
                }
            }    

        return formatted_postagem

    def delete(self, id):
        postagem = Postagem.query.get(id)
        db.session.delete(postagem)
        db.session.commit()
        return {}, 204

@ns.route("/tema")
class TemaListApi(Resource):
    @ns.marshal_list_with(tema_model)
    def get(self):
        temas = Tema.query.all()
        return temas
        
    @ns.expect(tema_input_model)
    @ns.marshal_with(tema_model)
    def post(self):
        print(ns.payload)
        tema = Tema(descricao=ns.payload["descricao"])
        db.session.add(tema)
        db.session.commit()
        return tema, 201

@ns.route("/tema/<int:id>")
class TemaApi(Resource):
    @ns.marshal_with(tema_model)
    def get(self, id):
        tema = Tema.query.get(id)
        if not tema:
            abort(404, message="Tema não encontrado")
        return tema
    
    @ns.expect(tema_input_model)
    @ns.marshal_with(tema_model)
    def put(self, id):
        tema = Tema.query.get(id)
        if not tema:
            abort(404, message="Tema não encontrado")
        tema.descricao = ns.payload["descricao"]
        db.session.commit()
        return tema

    def delete(self, id):
        tema = Tema.query.get(id)
        if not tema:
            abort(404, message="Tema não encontrado")
        db.session.delete(tema)
        db.session.commit()
        return {}, 204
