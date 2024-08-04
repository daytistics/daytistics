from flask_restful import Api
from flask import current_app, request, abort

api = Api(current_app)

current_app.logger.info(
    "The API is accessible from the following IP addresses: {} (Frontend), {} (Backend)".format(
        current_app.config.get("FRONTEND_IP"), current_app.config.get("BACKEND_IP")
    )
)


@current_app.before_request
def limit_remote_addr():
    with current_app.app_context():
        if request.remote_addr != current_app.config.get(
            "FRONTEND_IP"
        ) and request.remote_addr != current_app.config.get("BACKEND_IP"):
            abort(403)

try:
    from core.api import router
    router.load_routes(api)
except Exception as e:
    current_app.logger.error(f"Error while loading the API routes: {e}")