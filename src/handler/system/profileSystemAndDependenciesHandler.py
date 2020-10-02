from src.repository.system.systemRepository import SystemRepository
from src.repository.profileSystem.profileSystemRepository import ProfileSystemRepository
from src.repository.profilePermission.profilePermissionRepository import ProfilePermissionRepository
from src.repository.userProfileSystem.userProfileSystemRepository import UserProfileSystemRepository
from src import request
from src.infra.model.resultModel import ResultModel
from src.infra.handler.pagination import Paginate
from src.contract.profileSystemAndDependencies.createProfileSystemAndDependenciesContract import CreateProfileSystemAndDependenciesContract
from src.infra.handler.validationsAndSetStatusResultInfraHandler import ValidationsAndSetStatusResultInfraHandler


class ProfileSystemAndDependenciesHandler:

    def __init__(self):
        pass

    
    def create(self):
        contract = CreateProfileSystemAndDependenciesContract()
        playload = request.json
        if not(contract.validate(playload)):
            return ResultModel('Problema nos parametros enviados.', False, contract.errors).to_dict(), 406
        dto_profile_system = dict(
            system_id=playload.get('system_id'),
            name_profile_system=playload.get('name_profile_system'),
            description_profile_system=playload.get('description_profile_system')
        )
        
        repo_prof_sys = ProfileSystemRepository()
        repo_prof_sys.create(dto_profile_system)

        profile_system_db_result = repo_prof_sys.create(playload)
        status_result = ValidationsAndSetStatusResultInfraHandler()
        if (not profile_system_db_result['data']['result']):
            return status_result(profile_system_db_result)
        
        profile_system = profile_system_db_result['data']['result']
        profile_system_id = profile_system.get('id')
        system_permissions_id = playload.get('system_permissions_id')
        dto_multiple_profile_permission = []
        for permission_id in  system_permissions_id:
            dto_multiple_profile_permission.append(dict(
                system_permision_id=permission_id,
                profile_system_id=profile_system_id
            ))
        repo_prof_permis = ProfilePermissionRepository()
        prof_permis_db_result = repo_prof_permis.create(dto_multiple_profile_permission)
        if (not prof_permis_db_result['data']['result']):
            return status_result(prof_permis_db_result)
        profile_permission = prof_permis_db_result['data']['result']
        repo_user_prof_sys = UserProfileSystemRepository()
        dto_user_profile_system = dict(
            user_id=playload.get('user_id'),
            profile_system_id=profile_system_id
        )

        user_prof_sys_db_result = repo_user_prof_sys.create(dto_user_profile_system)
        if (not user_prof_sys_db_result['data']['result']):
            return status_result(user_prof_sys_db_result)
        user_profile_system = user_prof_sys_db_result['data']['result']
        data = dict(
            profile_system=profile_system,
            profile_permission=profile_permission,
            user_profile_system=user_profile_system
        )          
        return status_result.default(data)
        

    # def get_by_params(self):
    #     contract = GetByParamsSystemContract()
    #     playload = request.args
    #     if not(contract.validate(playload)):
    #         return ResultModel('Parametro incorreto.', False, contract.errors).to_dict(), 406
    #     params_filter = {}
    #     _id = playload.get('id')
    #     name = playload.get('name')
    #     url = playload.get('url')

    #     if _id:
    #         params_filter['id'] = _id
    #     if name:
    #         params_filter['name'] = name
    #     if url:
    #         params_filter['url'] = url
        
    #     repository = SystemRepository()
    #     systems = repository.get_search_by_params(params_filter)
        
    #     status_result = ValidationsAndSetStatusResultInfraHandler()
    #     return status_result.default(systems)
    
    # def delete(self):
    #     contract = DeleteSystemContract()
    #     playload = request.json
    #     if not(contract.validate(playload)):
    #         return ResultModel('Problema nos parametros enviados.', False, contract.errors).to_dict(), 406
    #     repository = SystemRepository()

    #     system = repository.delete(playload.get('id'))
        
    #     status_result = ValidationsAndSetStatusResultInfraHandler()
    #     return status_result.default(system)
