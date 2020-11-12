from flask import jsonify, current_app
from sqlalchemy.orm.exc import NoResultFound
from marshmallow import ValidationError

from library_api.lib.utilities import request_ids


def setup_handlers(app):

    @app.after_request
    def add_request_ids_to_header(response):
        # don't include request id on forbidden
        if response.status_code == 403:
            return response

        display_id, original_request_id = request_ids()
        if original_request_id:
            display_id = '{},{}'.format(original_request_id, display_id)

        response.headers.extend({'Request-Id': display_id})
        return response

    @app.errorhandler(ValidationError)
    def bad_data(e):
        current_app.logger.exception(e)
        return jsonify({"error": ['some errors'],
                        'message': 'Error: Data not valid.'}), 400

    @app.errorhandler(NoResultFound)
    def no_result_found(e):
        current_app.logger.exception(e)
        return jsonify({"error": "resource_not_found",
                        "message": "The requested resource could not be found"}), 404

    @app.errorhandler(422)
    def handle_validation_errors(e):
        return jsonify({'error': 'validation_failed',
                        'message': e.data['messages']}), 422

    @app.errorhandler(Exception)
    def internal_server_error(e):
        current_app.logger.exception(e)
        return jsonify({
            'message': "Apologies, there's been an unexpected error."}), 500

    @app.errorhandler(404)
    def resource_not_found(e):
        return jsonify(
            {'message': "The request resource was not found. "
             "Please check the URL."}), 404

    @app.errorhandler(401)
    def not_authorized(e):
        return jsonify(
            {'message': "The server could not verify that you are authorized "
             "to access the URL requested"}), 401
