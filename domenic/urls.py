"""
URL configuration for domenic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from edtech.views import login_view, termos_view, cadastro_aluno_view, home_view, editar_aluno_view, deletar_aluno_view, detalhes_curso_view, aluno_matricula_curso_view, pagamento_view, meus_cursos_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    path('termos/', termos_view, name='termos_servicos'),
    path('cadastro/', cadastro_aluno_view, name='cadastro'),
    path('home/', home_view, name='home'),
    path('home/<int:id_curso>/', detalhes_curso_view, name='detalhes_curso'),
    path('matricula/', aluno_matricula_curso_view, name='aluno_matricula_curso'),
    path('pagamento/<int:id_curso>/', pagamento_view, name='pagamento'),
    path('meus_cursos/', meus_cursos_view, name='meus_cursos'),
    path('meu_perfil/', editar_aluno_view, name="meu_perfil"),
    path('deletar_aluno/', deletar_aluno_view, name="deletar_aluno"),
]
