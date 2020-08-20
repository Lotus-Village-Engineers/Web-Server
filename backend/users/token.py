import six

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """ 유저 정보를 바탕으로 회원가입 인증 토큰 (원래는 비밀번호 재설정 토큰)을 생성한다. """
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.id) + six.text_type(timestamp) + six.text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()
