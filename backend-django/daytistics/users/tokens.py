from django.contrib.modules.users.tokens import PasswordResetTokenGenerator
import six


class AccountActivationGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
            + six.text_type(user.password)
        )


account_activation_token = AccountActivationGenerator()


class ChangePasswordGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.password)
        )


change_password_token = ChangePasswordGenerator()


class DeleteAccountGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # We are using the user's password as part of the hash value to make the hash unique
        return (
            six.text_type(user.pk)
            + six.text_type(timestamp)
            + six.text_type(user.is_active)
            + six.text_type(user.password)
        )


delete_account_token = DeleteAccountGenerator()
