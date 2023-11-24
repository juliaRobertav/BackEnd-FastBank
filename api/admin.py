from django.contrib import admin
from .models import Cadastro, Cliente, Transacao

# Register your models here.
admin.site.register(Cadastro)
admin.site.register(Cliente)
admin.site.register(Transacao)