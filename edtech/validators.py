import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def validate_strong_password(password):
    if len(password) < 8:
        raise ValidationError(_("A senha deve ter pelo menos 8 caracteres."))
    if not re.search(r'[A-Z]', password):
        raise ValidationError(_("A senha deve conter pelo menos uma letra maiúscula."))
    if not re.search(r'[a-z]', password):
        raise ValidationError(_("A senha deve conter pelo menos uma letra minúscula."))
    if not re.search(r'\d', password):
        raise ValidationError(_("A senha deve conter pelo menos um número."))
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(_("A senha deve conter pelo menos um caractere especial."))