from django.db import models

# Create your models here.

class Cadastro(models.Model):
    nome = models.CharField(max_length=50)
    nasc = models.CharField(max_length=50)
    cpf = models.IntegerField()
    email = models.CharField(max_length=50)
    senha = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.nome} - {self.cliente} - R$ {self.saldo}'
    
    

class Cliente(models.Model):
    
    def upload_imagem_cliente(instance, filename):
        return f"{instance.conta}-{filename}"

    nome = models.CharField(max_length=120)
    conta = models.CharField(max_length=10, unique=True)
    limite = models.FloatField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    ultima_movimentacao = models.DateTimeField(auto_now_add=True)
    imagem = models.ImageField(upload_to=upload_imagem_cliente, blank=True, null=True)

    def __str__(self):
        return self.conta
    
    
    
class Transacao(models.Model):

    conta_cliente = models.ForeignKey(Cliente, null=True, verbose_name='Cliente', related_name='transacoes',
                                       on_delete=models.PROTECT)
    descricao = models.CharField(max_length=120, null=False)
    valor = models.FloatField(null=False)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.conta_cliente


class Contas(models.Model):
    agencia = models.CharField(max_length=10)
    cliente = models.OneToOneField('Cliente', on_delete=models.CASCADE)
    conta = models.CharField(max_length=10)
    saldo = models.DecimalField(decimal_places=2, max_digits=30, default=0.00)
    ultima_movimentacao = models.DateTimeField(auto_now=True)
    
    def __str__(self) :
        return f'{str(self.agencia)}/{str(self.conta)}'
    
    def get_ultima_movimentacao(self):
        return self.ultima_movimentacao.strftime('%d/%m/%Y %H:%M')
    
    
# class Saldo(models.Model):
#     cliente = models.OneToOneField('Cliente', on_delete=models.CASCADE, related_name='saldo_associado')
#     saldo = models.DecimalField(max_digits=10, decimal_places=2)
#     ultima_movimentacao = models.DateTimeField()
    
#     def __str__(self):
#         return f'{self.cliente} - R$ {self.saldo}'


class Deposito(models.Model):
    conta = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    valor = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    data_deposito = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'{str(self.conta)}'
    
    def get_data_deposito(self):
        return self.data_deposito.strftime('%d/%m/%Y %H:%M')
    
    