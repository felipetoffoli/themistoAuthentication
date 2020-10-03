from src.model.profileSystem import ProfileSystem
from src import db
from flask import current_app
from flask_restful import marshal
from src.model.schemas import PAGINATE
from src.model.schemas.systemPermission import profile_system_fields
from src.infra.model.resultModel import ResultModel


class ProfileSystemRepository:
    

    def get_all(self, playload):
        try:
            page = playload.get('page')
            per_page = playload.get('per_page')

            profile_system = ProfileSystem.query.filter().paginate(page, per_page)
            data_paginate = marshal(profile_system, PAGINATE)
            data = marshal(profile_system.items, profile_system_fields)
            return ResultModel('Pesquisa realizada com sucesso.', data, False).to_dict(data_paginate)
        except Exception as e:
            return ResultModel('Não foi possivel realizar a pesquisa.', False, True, str(e)).to_dict()

    def get_search_by_params(self, playload, witch_dates=False):
        try:
            page = playload.get('page')
            per_page = playload.get('per_page')
           
            profile_system = ProfileSystem.query.filter_by(playload).all()
            data_paginate = marshal(profile_system, PAGINATE)
            data = marshal(profile_system.items, profile_system_fields)
            return ResultModel('Pesquisa realizada com sucesso.', data, False).to_dict(data_paginate)
        except Exception as e:
            return ResultModel('Não foi possivel realizar a pesquisa.', False, True, str(e)).to_dict()

    def create(self, playload):
        try:
            system_id = playload.get('system_id')
            name = playload.get('name')

            profile_system_exist = ProfileSystem.query.filter_by(system_id=system_id, name=name).first()
            if profile_system_exist:
                return ResultModel(f'Esses dados já foram cadastrados.', False, True).to_dict()
           
            profile_system = ProfileSystem(playload)
            db.session.add(profile_system)
            db.session.commit()
            data = marshal(profile_system, profile_system_fields)
            return ResultModel('Criado com sucesso.', data, False).to_dict()
        except Exception as e:
            return ResultModel('Não foi possivel criar.', False, True, str(e)).to_dict()
    

    def update(self, playload):
        try:
            _id = playload.get('id')
            system_id = playload.get('system_id')
            name = playload.get('name')
            description = playload.get('description')
            profile_system = ProfileSystem.query.get(_id)
            if not profile_system:
                return ResultModel('Id não encontrado.', False, True).to_dict()
            
            profile_system.system_id = system_id
            profile_system.name = name
            profile_system.description = description
            db.session.add(profile_system)
            db.session.commit()
            data = marshal(profile_system, profile_system_fields)
            return ResultModel('Atualizado com sucesso.', data, False).to_dict()
        except Exception as e:
            return ResultModel('Não foi possivel atualizar.', False, True, str(e)).to_dict()

    def delete(self, _id):
        try:
            profile_system = ProfileSystem.query.get(_id)
            if not profile_system:
                return ResultModel('Não encontrado.', False, True).to_dict()
            db.session.delete(profile_system)
            db.session.commit()
            data = marshal(profile_system, profile_system_fields)
            return ResultModel('Deletado com sucesso.', data, False).to_dict()
        except Exception as e:
            return ResultModel('Não foi possivel deletar.', False, True, str(e)).to_dict()