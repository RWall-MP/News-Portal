from allauth.account.forms import SignupForm
from django.contrib.auth.models import User
from django.core.mail import send_mail


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)

        send_mail(
            subject='Добро пожаловать на наш новостной портал!',
            message=f'{user.username}, вы успешно зарегистрировались!',
            from_email=None,
            recipient_list=[user.email],
        )
        return user

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
