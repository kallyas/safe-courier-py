from flask import Blueprint, jsonify, request

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource at {} not found'.format(request.path)}), 404


@errors.app_errorhandler(405)
def method_not_allowed(error):
    return jsonify({'error': 'Method {} not allowed on this resource'.format(request.method)}), 405


@errors.app_errorhandler(500)
def internal_server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


@errors.app_errorhandler(403)
def forbidden(error):
    return jsonify({'error': 'Access to this resource is forbidden'}), 403


@errors.app_errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400