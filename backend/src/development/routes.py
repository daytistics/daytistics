from flask import Flask, request, current_app
from src.development import bp
from src.models.users import register_user
from src.utils.emails import send_verification_email


# @bp.route('/development/register', methods=['GET', 'POST'])
# def register():
#     try:
#         with current_app.app_context():
#             email = request.args.get('email')
#             send_code_email(email, "123456")
#             return f'Testing user registration with email: {email}'
#     except Exception as e:
#         return str(e)

#     register_user("Leo", "GueltigesTestpasswort01!", email)