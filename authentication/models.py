from djongo import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UsuarioManager(BaseUserManager):
    def create_user(self, rfc, nombre, aPaterno, aMaterno, email, password=None):
        if not rfc:
            raise ValueError("El RFC es obligatorio")
        if not nombre:
            raise ValueError("El nombre es obligatorio")
        if not aPaterno:
            raise ValueError("El apellido paterno es obligatorio")
        if not aMaterno:
            raise ValueError("El apellido materno es obligatorio")
        if not email:
            raise ValueError("El email es obligatorio")
        if len(rfc) < 13:
            raise ValueError("El RFC debe contener 13 caracteres")

        usuario = self.model(
            nombre = nombre,
            aPaterno = aPaterno,
            aMaterno = aMaterno,
            rfc = rfc,
            email = self.normalize_email(email),
        )

        usuario.set_password(password)
        usuario.save(using=self._db)

        return usuario

    def create_superuser(self, rfc, nombre, aPaterno, aMaterno, email, password):
        usuario = self.create_user(
            rfc=rfc,
            nombre=nombre,
            aPaterno=aPaterno,
            aMaterno=aMaterno,
            email=email,
            password=password
        )

        usuario.save(using= self._db)
        return usuario

class Usuarios(AbstractBaseUser):
    _id = models.ObjectIdField()
    nombre = models.TextField()
    aPaterno = models.TextField()
    aMaterno = models.TextField()
    #password = models.TextField()
    rfc = models.TextField(unique=True, max_length=13)
    email = models.TextField(verbose_name='email')
    
    USERNAME_FIELD = 'rfc'
    REQUIRED_FIELDS = ['nombre','aPaterno', 'aMaterno', 'email']

    objects = UsuarioManager()

    def __str__(self):
        return self.nombre + " " + self.aPaterno + " " + self.aMaterno
   