from allauth.account.forms import SignupForm, LoginForm
from django_recaptcha.fields import ReCaptchaField

class CustomSignupForm(SignupForm):
    captcha = ReCaptchaField()

    def save(self, request):
        return super().save(request)

class CustomLoginForm(LoginForm):
    captcha = ReCaptchaField()