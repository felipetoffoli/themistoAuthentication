from src.model.users import User
from src.model.person import Person
from src import db
from flask_bcrypt import Bcrypt
from flask import current_app
from flask_restful import marshal
from src.model.schemas import PAGINATE
from src.model.schemas.users import users_fields, users_fields_with_pass
from src.infra.model.resultModel import ResultModel


class UserRepository:
    

    def get_all(self, playload):
        try:
            paginate_filter = playload.get('paginate')
            users = User.query.filter().paginate(**paginate_filter)
            data_paginate = marshal(users, PAGINATE)
            data = marshal(users.items, users_fields)
            return ResultModel('Pesquisa realizada com sucesso.', data, False).to_dict(data_paginate)
        except Exception as e:
            return ResultModel('Não foi possivel realizar a pesquisa.', False, True, str(e)).to_dict()

    def get_by_username(self, username, witch_password=False):
        try:
            schemas_user = users_fields
            if witch_password:
                schemas_user = users_fields_with_pass
        
            user = User.query.filter_by(username=username).first()
            if not user:
                return ResultModel('Nome de usuario não encontrado.', False, True).to_dict()
            data = marshal(user, schemas_user)
            return ResultModel('Pesquisa realizada com sucesso.', data, False).to_dict()
        except Exception as e:
            return ResultModel('Não foi possivel realizar a pesquisa.', False, True, str(e)).to_dict()
            
    def get_by_id(self, _id):
        try:
            users = User.query.get(_id).first()
            data = marshal(users, users_fields)
            return ResultModel('Pesquisa realizada com sucesso.', data, False).to_dict()
        except Exception as e:
            return ResultModel('Não foi possivel realizar a pesquisa.', False, True, str(e)).to_dict()
    
    def search_multiples_ids(self, playload):
        try:
            ids = playload.get('ids')
            users = User.query.filter(User.id.in_(ids)).all()
            data_paginate = marshal(users, PAGINATE)
            data = marshal(users, users_fields)
            return ResultModel('Pesquisa realizada com sucesso.', data, False).to_dict(data_paginate)
        except Exception as e:
            return ResultModel('Não foi possivel realizar a pesquisa.', False, True, str(e)).to_dict()

    def create(self, playload):
        try:
            username = playload.get('username')
            password = playload.get('password')
            is_admin = playload.get('is_admin')
            person_id = playload.get('person_id')
            user = User.query.filter_by(username=username).first()
            if user:
                return ResultModel(f'Usuario "{username}" já existe.', False, True).to_dict()
            person = Person.query.get(person_id)
            if not person:
                return ResultModel(f'Pessoa não encontrada.', False, True).to_dict()
            user = User(username, password, is_admin, person_id)
            db.session.add(user)
            db.session.commit()
            data = marshal(user, users_fields)
            return ResultModel('Usuario criado com sucesso.', data, False).to_dict()
        except Exception as e:
            return ResultModel('Não foi possivel criar o usuario.', False, True, str(e)).to_dict()
    
    def get_by_id(self, _id):
        try:
            user = User.query.get(_id)
            if not user:
                return ResultModel('Usuario não existe.', False, True).to_dict()
            data =  marshal(user, users_fields)
            return ResultModel('Pesquisa realizada com sucesso.', data, False).to_dict()
        except Exception as e:
            return ResultModel('Não foi possivel realizar a pesquisa.', False, True, str(e)).to_dict()

    def update(self, _id, username, password, is_admin):
        try:
            user = User.query.get(_id)
            if not user:
                return ResultModel('Usuario não existe.', False, True).to_dict()
            bcrypt = Bcrypt(current_app)
            user.username = username
            user.password = bcrypt.generate_password_hash(password).decode('utf-8')
            user.is_admin = is_admin
            db.session.add(user)
            db.session.commit()
            data = marshal(user, users_fields)
            return ResultModel('Usuario atualizado com sucesso.', data, False).to_dict()
        except Exception as e:
            return ResultModel('Não foi possivel atualizar o usuario.', False, True, str(e)).to_dict()

    def delete(self, _id):
        try:
            user = User.query.get(_id)
            if not user:
                return ResultModel('Usuario não existe.', False, True).to_dict()
            db.session.delete(user)
            db.session.commit()
            data = marshal(user, users_fields)
            return ResultModel('Usuario deletado com sucesso.', data, False).to_dict()
        except Exception as e:
            return ResultModel('Não foi possivel deletar o usuario.', False, True, str(e)).to_dict()
