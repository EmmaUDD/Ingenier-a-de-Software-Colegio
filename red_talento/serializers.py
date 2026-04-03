from rest_framework_simplejwt.serializers import( 
    TokenObtainPairSerializer
)
from rest_framework import serializers
from .models import Usuario, PerfilEstudiante, PerfilDocente, PerfilEmpresa


class TokenRole(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token


class RegistroEstudianteSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    especialidad = serializers.CharField(required=True)
    grado = serializers.ChoiceField(choices=['4to_medio', 'egresado'], default='4to_medio')

    def create(self, validated_data):
        especialidad = validated_data.pop('especialidad')
        grado = validated_data.pop('grado')
        usuario = Usuario.objects.create_user(**validated_data, role='estudiante')
        PerfilEstudiante.objects.create(usuario=usuario, especialidad=especialidad, grado=grado)
        return usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'first_name', 'last_name', 'email']

class PerfilEstudianteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()  # anidado
    
    class Meta:
        model = PerfilEstudiante
        fields = '__all__'


class RegistroDocenteSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    departamento = serializers.CharField(required=True)
    bio  = serializers.CharField(required=False)

    def create(self, validated_data):
        departamento = validated_data.pop('departamento')
        bio = validated_data.pop('bio', None)
        usuario = Usuario.objects.create_user(**validated_data, role='docente')
        PerfilDocente.objects.create(usuario=usuario, departamento=departamento, bio=bio)
        return usuario
    
class RegistroEmpresaSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    nombre_empresa = serializers.CharField(required=True)
    industria  = serializers.CharField(required=True)
    rut = serializers.CharField(required=True)

    def create(self, validated_data):
        nombre_empresa = validated_data.pop('nombre_empresa')
        industria = validated_data.pop('industria')
        rut = validated_data.pop('rut')
        usuario = Usuario.objects.create_user(**validated_data, role='empresa')
        PerfilEmpresa.objects.create(usuario=usuario, nombre_empresa=nombre_empresa, industria=industria, rut=rut)
        return usuario


