from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(HTTPException)
    def http_error(e):
        return jsonify({"error": e.name, "message": e.description}), e.code

    @app.errorhandler(Exception)
    def unhandled(e):
        app.logger.exception(e)
        return jsonify({"error": "InternalServerError"}), 500
