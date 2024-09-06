
from django.shortcuts import render, redirect
from .forms import LoginForm, CadastroForm, EditarForm
import requests 
from django.contrib import messages
from datetime import datetime

URL_BASE = 'https://domenic-edtech-backend-apim.azure-api.net'

def login_obrigatorio(funcao):
    def wrapper(request, *args, **kwargs):
        if request.session.get('is_authenticated'):
            return funcao(request, *args, **kwargs)
        
        return redirect('login')
    return wrapper

def pagamento_obrigatorio(funcao):
    def wrapper(request, *args, **kwargs):
        if request.session.get('is_pago'):
            return funcao(request, *args, **kwargs)
        
        return redirect('home')
    return wrapper

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            payload = {
                "email": form.cleaned_data.get('email'),
                "senha": form.cleaned_data.get('senha')
            }

            response = requests.get(URL_BASE + '/get_login_aluno', params=payload)

            if response.ok:
                request.session['id_aluno'] = response.json()['Mensagem']['id_aluno']
                request.session['nome_completo'] = response.json()['Mensagem']['nome_completo']
                request.session['data_nascimento'] = response.json()['Mensagem']['data_nascimento']
                request.session['celular'] = response.json()['Mensagem']['celular']
                request.session['endereco'] = response.json()['Mensagem']['endereco']
                request.session['cpf'] = response.json()['Mensagem']['cpf']
                request.session['email'] = form.cleaned_data.get('email')    
                request.session['is_authenticated'] = True       
                return redirect('home')
            
            messages.error(request, 'E-mail ou senha incorretos!')

    return render(request, 'edtech/login.html', {'form': form})

def termos_view(request):
    return render(request, 'edtech/termos_servicos.html')

def cadastro_aluno_view(request):
    form = CadastroForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            nome_completo = form.cleaned_data.get('nome_completo')
            data_nascimento_raw = form.cleaned_data.get('data_nascimento')
            data_nascimento = data_nascimento_raw.strftime('%m/%d/%Y')
            celular = form.cleaned_data.get('celular')
            endereco = form.cleaned_data.get('endereco')
            cpf = form.cleaned_data.get('cpf')
            foto_perfil = form.cleaned_data.get('foto_perfil')
            email = form.cleaned_data.get('email')
            senha = form.cleaned_data.get('senha')

            json_payload = {
                "nome_completo": nome_completo,
                "data_nascimento": data_nascimento,
                "celular": celular,
                "endereco": endereco,
                "cpf": cpf,
                "foto_perfil": foto_perfil,
                "email": email,
                "senha": senha
            }
            
            response = requests.post(URL_BASE + '/create_aluno', json = json_payload, headers={'Content-type': 'application/json', 'Accept': '*/*'})

            if response.ok:            
                return redirect('login')
            
    return render(request, 'edtech/cadastro.html', {'form': form})

@login_obrigatorio
def editar_aluno_view(request):
    form = EditarForm(request.POST or None, initial={
        'nome_completo': request.session.get('nome_completo'),
        'data_nascimento': datetime.strptime(request.session.get('data_nascimento'), '%m/%d/%Y').date(),
        'celular': request.session.get('celular'),
        'endereco': request.session.get('endereco'),
        'cpf': request.session.get('cpf'),
        'email': request.session.get('email'),
    })

    if request.method == "POST":
        if form.is_valid():
            nome_completo = form.cleaned_data.get('nome_completo')
            data_nascimento_raw = form.cleaned_data.get('data_nascimento')
            data_nascimento = data_nascimento_raw.strftime('%m/%d/%Y')
            celular = form.cleaned_data.get('celular')
            endereco = form.cleaned_data.get('endereco')
            cpf = form.cleaned_data.get('cpf')
            foto_perfil = form.cleaned_data.get('foto_perfil')
            email = form.cleaned_data.get('email')
            senha = form.cleaned_data.get('senha')

            json_payload = {
                "nome_completo": nome_completo,
                "data_nascimento": data_nascimento,
                "celular": celular,
                "endereco": endereco,
                "cpf": cpf,
                "foto_perfil": foto_perfil,
                "email": email,
                "senha": senha
            }
            
            response = requests.post(URL_BASE + '/edit_aluno', params={'id_aluno': request.session.get('id_aluno')}, json = json_payload, headers= {'Content-type': 'application/json', 'Accept': '*/*'})

            if response.ok:            
                request.session['nome_completo'] = nome_completo
                request.session['data_nascimento'] = data_nascimento
                request.session['celular'] = celular
                request.session['endereco'] = endereco
                request.session['cpf'] = cpf
                request.session['email'] = email
                return redirect('home')
            
            messages.error(request, 'Erro ao editar o aluno!')
        
    return render(request, 'edtech/meu_perfil.html', {'form': form, 'nome_completo': request.session.get('nome_completo'), 'email': request.session.get('email')})

@login_obrigatorio
def deletar_aluno_view(request):
    if request.method == "POST":

        response_matricula = requests.post(URL_BASE + '/delete_aluno_matricula_curso', params={'id_aluno': request.session.get('id_aluno')})

        if response_matricula:
            response_aluno = requests.post(URL_BASE + '/delete_aluno', params={'id_aluno': request.session.get('id_aluno')})

            if response_aluno.ok:
                del request.session['nome_completo']
                del request.session['data_nascimento']
                del request.session['celular']
                del request.session['endereco']
                del request.session['cpf']
                del request.session['email']
                request.session['is_pago'] = False
                request.session['is_authenticated'] = False
                return redirect('login')
            
            messages.error(request, 'Erro ao deletar o aluno!')

        messages.error(request, 'Erro ao deletar a matricula!')

    return render(request, 'edtech/meu_perfil.html')

def get_professor_id(id_professor):
    response = requests.get(URL_BASE + '/get_professores_id', params={'id_professor': id_professor})

    if response.ok:
        data = response.json()['Mensagem']
        return data

@login_obrigatorio
def home_view(request):

    response = requests.get(URL_BASE + '/get_cursos')

    cursos_novo = []

    if response.ok:
        cursos = response.json()['Mensagem']
        for curso in cursos:
            curso['prof_nome_completo'] = get_professor_id(curso['id_professor'])['nome_completo']
            cursos_novo.append(curso)
    else:
        cursos = []
    messages.error(request, 'Erro ao buscar os cursos!')

    return render(request, 'edtech/home.html', {'cursos': cursos_novo})

@login_obrigatorio
def detalhes_curso_view(request, id_curso):

    response = requests.get(URL_BASE + '/get_curso_id', params={'id_curso': id_curso})
    
    if response.ok:
        curso = response.json()['Mensagem'] 
        curso['prof_nome_completo'] = get_professor_id(curso['id_professor'])['nome_completo']
        curso['prof_foto_perfil'] = get_professor_id(curso['id_professor'])['foto_perfil']
        curso['prof_bio'] = get_professor_id(curso['id_professor'])['bio']
    else:
        curso = None

    
    return render(request, 'edtech/detalhes_curso.html', {'curso': curso})

@login_obrigatorio
def aluno_matricula_curso_view(request):  
    return render(request, 'edtech/detalhes_curso.html')


@login_obrigatorio
def pagamento_view(request, id_curso):
    response = requests.post(URL_BASE + '/aluno_matricula_curso', params={'id_curso': id_curso, 'id_aluno': request.session.get('id_aluno')})

    if response.ok:
        request.session['is_pago'] = True
        return redirect('pagamento', id_curso = id_curso) 
    
   
    return render(request, 'edtech/pagamento.html')

@login_obrigatorio
@pagamento_obrigatorio
def meus_cursos_view(request):

    response = requests.get(URL_BASE + '/get_curso_id', params={'id_aluno': request.session.get('id_aluno')})

    cursos_novo = []

    if response.ok:
        cursos = response.json()['Mensagem']
        for curso in cursos:
            curso['prof_nome_completo'] = get_professor_id(curso['id_professor'])['nome_completo']
            cursos_novo.append(curso)
    else:
        cursos = []

    return render(request, 'edtech/meus_cursos.html', {'cursos': cursos_novo})

