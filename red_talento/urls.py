from django.urls import path
from .views import (
    RegistroEstudianteView, 
    RegistroDocenteView, 
    RegistroEmpresaView,
    ActivarEstudianteView,
    PerfilEstudianteView,
)


urlpatterns = [
    path('registro/estudiante/', RegistroEstudianteView.as_view(), name='registro_estudiante'),
    path('registro/docente/', RegistroDocenteView.as_view(), name='registro_docente'),
    path('registro/empresa/', RegistroEmpresaView.as_view(), name='registro_empresa'),
    path('estudiantes/<int:id>/activar/', ActivarEstudianteView.as_view(), name='activar_estudiante'),
    path('perfil/estudiante/<int:id>/', PerfilEstudianteView.as_view(), name='perfil_estudiante'),


]