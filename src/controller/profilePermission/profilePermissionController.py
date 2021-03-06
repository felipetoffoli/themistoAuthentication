from flask import Blueprint, jsonify, request
from flask_jwt_extended import  jwt_required
from flask import current_app, request
from src.infra.decorator.auth.authDecorator import AuthDecorator
from src.handler.profilePermission.profilePermissionHandler import ProfilePermissionHandler as ProfilePermission
from src.infra.decorator.request.errorsRequestDecorator import ErrorsRequestDecorator
from src.model.enum.permission import PermissionEnum

controller_profile_permission = Blueprint('controller_profile_permission', __name__)
jwt = AuthDecorator()
validity_req = ErrorsRequestDecorator()


@controller_profile_permission.route('/profilepermission', methods=['GET'])
@jwt.required_permission(PermissionEnum.VIEW.value)
def get_all():
    return  ProfilePermission().get_all() 

@controller_profile_permission.route('/profilepermission/params', methods=['GET'])
@jwt.required_permission(PermissionEnum.VIEW.value)
def get_by_params():
    return  ProfilePermission().get_by_params() 

@controller_profile_permission.route('/profilepermission', methods=['PUT'])
@jwt.required_permission(PermissionEnum.EDIT.value)
@validity_req.body_is_json
def update():
    return  ProfilePermission().update()

@controller_profile_permission.route('/profilepermission', methods=['POST'])
@jwt.required_permission(PermissionEnum.CRAFT.value)
@validity_req.body_is_json
def create():
    return  ProfilePermission().create()

@controller_profile_permission.route('/profilepermission', methods=['DELETE'])
@jwt.required_permission(PermissionEnum.DEL.value)
@validity_req.body_is_json
def delete_by_id():
    return  ProfilePermission().delete() 


