# accounts/forms.py
from django import forms
from .validators import validate_strong_password

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Digite seu E-mail'}))
    senha = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'}))

class CadastroForm(forms.Form):
    nome_completo = forms.CharField(label='Nome Completo', max_length=300, required=True, widget=forms.TextInput(attrs={'placeholder': 'Digite seu Nome Completo'}))
    data_nascimento = forms.DateField(label='Data de Nascimento', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    celular = forms.CharField(label='Celular', max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Digite seu Celular'}))
    endereco = forms.CharField(label='Endereco', max_length=300, required=True, widget=forms.TextInput(attrs={'placeholder': 'Digite seu Endereço'}))
    cpf = forms.CharField(label='CPF', max_length=14, required=True, widget=forms.TextInput(attrs={'placeholder': 'Digite seu CPF'}))
    foto_perfil = forms.ImageField(label='Foto de Perfil', required=False)
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Digite seu E-mail'}))
    senha = forms.CharField(label='Senha', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua Senha'}), validators=[validate_strong_password])

class EditarForm(forms.Form):
    nome_completo = forms.CharField(label='Nome Completo', max_length=300, required=True, widget=forms.TextInput(attrs={'placeholder': 'Digite seu Nome Completo'}))
    data_nascimento = forms.DateField(label='Data de Nascimento', required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    celular = forms.CharField(label='Celular', max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': 'Digite seu Celular'}))
    endereco = forms.CharField(label='Endereco', max_length=300, required=True, widget=forms.TextInput(attrs={'placeholder': 'Digite seu Endereço'}))
    cpf = forms.CharField(label='CPF', max_length=14, required=True, widget=forms.TextInput(attrs={'placeholder': 'Digite seu CPF'}))
    email = forms.EmailField(label='Email', required=True, widget=forms.EmailInput(attrs={'placeholder': 'Digite seu E-mail'}))
    foto_perfil = forms.ImageField(label='Foto de Perfil', required=False)
    senha = forms.CharField(label='Senha', required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua Senha'}), validators=[validate_strong_password])