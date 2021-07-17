from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import PasswordInput
from django.contrib.auth import authenticate
from account.models import Account


class RegistrationForm(UserCreationForm):
    email_errors = {
        'required': 'Обязательное поле.',
        'invalid': 'Проверьте введенные данные.',
        'unique': 'Такая почта уже зарегистрирована.'
    }
    username_errors = {
        'required': 'Обязательное поле.',
        'invalid': 'Проверьте введенные данные.',
        'unique': 'Имя пользователя уже занято.'
    }
    email = forms.EmailField(error_messages=email_errors, max_length=60, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Email', }))
    username = forms.CharField(error_messages=username_errors, max_length=30, required=True,
                               widget=forms.TextInput(attrs={'placeholder': "Имя пользователя", 'autocomplete': 'off'}))

    class Meta:
        model = Account
        fields = [
            'email',
            'username',
            'password1',
            'password2'
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = PasswordInput(attrs={'placeholder': 'Пароль', 'autocomplete': 'off'})
        self.fields['password2'].widget = PasswordInput(
            attrs={'placeholder': 'Подтвердите пароль', 'autocomplete': 'off'})
        self.fields['email'].widget.attrs.update({'autofocus': False})


class AccountAuthenticationForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Пароль'}))

    class Meta:
        model = Account
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            email_exists_req = Account.objects.filter(email=email)
            email_is_active_req = Account.objects.filter(email=email, is_active=False)
            if not authenticate(email=email, password=password):
                if not email_exists_req.exists():
                    raise forms.ValidationError("Указанная почта не была зарегистрирована")
                if email_is_active_req.exists():
                    raise forms.ValidationError("Ваша учетная запись была деактивирована")
                raise forms.ValidationError("Неправильно указана почта или пароль")


class AccountUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
 'placeholder': 'Имя пользователя'
    }))
    class Meta:
        model = Account
        fields = ('email', 'username')

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError("Такая электронная почта уже используется")

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError("Такое имя пользователя уже используется")
