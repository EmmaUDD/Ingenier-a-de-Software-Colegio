from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    RegistroEstudianteSerializer, 
    RegistroEmpresaSerializer, 
    RegistroDocenteSerializer, 
    TokenRole,
    PerfilEstudianteSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Usuario, PerfilEstudiante
from .permissions import EsDocente
from rest_framework.permissions import IsAuthenticated

class LoginView(TokenObtainPairView):
    serializer_class = TokenRole

class ActivarEstudianteView(APIView):
    permission_classes = [IsAuthenticated, EsDocente]
    def patch(self, request, id):
        try:
            usuario = Usuario.objects.get(id=id, role='estudiante')
        except Usuario.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
        usuario.is_active = True
        usuario.save()
        return Response({'mensaje': 'Estudiante activado'}, status=status.HTTP_200_OK)


# Create your views here.
class RegistroEstudianteView(APIView):
    def post(self, request):
        serializer = RegistroEstudianteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Estudiante registrado'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PerfilEstudianteView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            perfil = PerfilEstudiante.objects.get(id=id)
        except PerfilEstudiante.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PerfilEstudianteSerializer(perfil)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, id):
        try:
            perfil = PerfilEstudiante.objects.get(id=id)
        except PerfilEstudiante.DoesNotExist:
            return Response({'error': 'Estudiante no encontrado'}, status=status.HTTP_404_NOT_FOUND)  
        if perfil.usuario != request.user:
            return Response({'error': 'No autorizado'}, status=status.HTTP_403_FORBIDDEN)
        serializer = PerfilEstudianteSerializer(perfil, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class RegistroDocenteView(APIView):
    def post(self, request):
        serializer = RegistroDocenteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Docente registrado'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegistroEmpresaView(APIView):
    def post(self, request):
        serializer = RegistroEmpresaSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'mensaje': 'Empresa registrada'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)