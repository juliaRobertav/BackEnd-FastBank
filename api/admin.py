from django.contrib import admin
from .models import Cadastro, Cliente, Transacao, Deposito, Saque, Emprestimo, Credito, Login

# Register your models here.
admin.site.register(Cadastro)
admin.site.register(Cliente)
admin.site.register(Transacao)
admin.site.register(Deposito)
admin.site.register(Saque)
admin.site.register(Emprestimo)
admin.site.register(Credito)
admin.site.register(Login)
