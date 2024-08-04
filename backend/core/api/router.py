from flask_restful import Api

def load_routes(api: Api) -> None:
    """
    Load routes for the API.

    Args:
        api (Api): The Flask-Restful Api object.

    Returns:
        None
    """
    from core.api.resources import users
    from core.utils import routes

    api.add_resource(users.UserCheckPassword, routes.CHECK_PASSWORD_ROUTE)
    api.add_resource(users.GetUserInformation, routes.GET_USER_INFORMATION_ROUTE)
    api.add_resource(users.RefreshUserToken, routes.REFRESH_USER_TOKEN_ROUTE)
    api.add_resource(users.GetUserEmail, routes.GET_USER_EMAIL_ROUTE)
    api.add_resource(users.ExistsUser, routes.EXISTS_USER_ROUTE)
    api.add_resource(
        users.ResendRegistrationEmail, routes.RESEND_REGISTRATION_EMAIL_ROUTE
    )
    api.add_resource(users.ExistsRegistrationRequest, routes.EXISTS_REGISTRATION_REQUEST_ROUTE)
    api.add_resource(users.RegisterUser, routes.REGISTER_USER_ROUTE)
    api.add_resource(users.LoginUser, routes.LOGIN_USER_ROUTE)
    api.add_resource(
        users.VerifyRegistrationRequest, routes.VERIFY_REGISTRATION_ROUTE
    )
    api.add_resource(
        users.HasExceededFailureLimit, routes.HAS_EXCEEDED_FAILURE_LIMIT_ROUTE
    )