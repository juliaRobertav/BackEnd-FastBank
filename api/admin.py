from django.contrib import admin
from .models import Cadastro, Cliente, Transacao, Contas, Deposito, Saque, Emprestimo, Credito

# Register your models here.
admin.site.register(Cadastro)
admin.site.register(Cliente)
admin.site.register(Transacao)
admin.site.register(Contas)
admin.site.register(Deposito)
admin.site.register(Saque)
admin.site.register(Emprestimo)
admin.site.register(Credito)