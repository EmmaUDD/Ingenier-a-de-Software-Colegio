from rest_framework.permissions import BasePermission
from .models import Usuario

class EsDocente(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'docente'

class EsEstudiante(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'estudiante'

class EsEmpresa(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'empresa'


