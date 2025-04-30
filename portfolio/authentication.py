from rest_framework.authentication import SessionAuthentication
from whitenoise

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return
