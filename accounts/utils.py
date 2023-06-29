import threading
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class VerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.id)+six.text_type(timestamp)+six.text_type(user.is_verified)
verification_token=VerificationTokenGenerator()        

class PasswordTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.id)+six.text_type(timestamp)+six.text_type(user.password)+six.text_type(user.is_verified)

password_reset_token=PasswordTokenGenerator()









class EmailThread(threading.Thread):

    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()