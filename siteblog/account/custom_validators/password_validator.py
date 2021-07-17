from django.contrib.auth.password_validation import MinimumLengthValidator
from django import forms
from django.utils.translation import ugettext as _


class CustomPasswordValidator:

    def __init__(self, min_length=1):
        self.min_length = min_length

    def validate(self, password, user=None):
        special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
        if not any(char.isdigit() for char in password):
            raise forms.ValidationError(
                _('В пароле должна быть минимум %(min_length)d цифра.') % {'min_length': self.min_length})
        if not any(char.isalpha() for char in password):
            raise forms.ValidationError(
                _('Пароль не должен состоять только из цифр.'))
        if not any(char.isupper() for char in password):
            raise forms.ValidationError(
                _('В пароле должна быть как минимум %(min_length)d заглавная буква.') % {'min_length': self.min_length})
        if not any(char.islower() for char in password):
            raise forms.ValidationError(
                _('В пароле должна быть как минимум %(min_length)d строчная буква.') % {'min_length': self.min_length})
        if not any(char in special_characters for char in password):
            raise forms.ValidationError(
                _('В пароле должен быть минимум %(min_length)d спецсимвол.') % {'min_length': self.min_length})

    def get_help_text(self):
        return ""


class CustomPasswordLengthValidator(MinimumLengthValidator):

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise forms.ValidationError(
                _("Пароль не может быть короче %(min_length)d символов."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return ""
