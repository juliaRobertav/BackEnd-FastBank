from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

#TESTAR: 

class Endereco(models.Model):
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.cidade}/{self.estado} - CEP: {self.cep}'
    
    
# class Cadastro(models.Model):
    
#     def upload_imagem_cliente(instance, filename):
#         return f"{instance.conta}-{filename}"
    
#     nome = models.CharField(max_length=50)
#     nasc = models.CharField(max_length=50)
#     cpf = models.IntegerField()
#     email = models.CharField(max_length=50)
#     senha = models.CharField(max_length=50)
    
#     conta = models.CharField(max_length=10, unique=True, default='00000000')
#     limite = models.FloatField(null=True)
#     # criado_em = models.DateTimeField(auto_now_add=True)
#     agencia = models.CharField(max_length=10,  default='0000')
#     # ultima_movimentacao = models.DateTimeField(auto_now_add=True)
#     saldo = models.DecimalField(decimal_places=2, max_digits=30, default=0.00)
#     telefone = models.CharField(max_length=15, default=000.000000)
#     imagem = models.ImageField(upload_to=upload_imagem_cliente, blank=True, null=True)
#     endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, null=True)  
    
#     def __str__(self):
#         return f'{self.nome} - {self.endereco} - {self.telefone} - R$ {self.saldo}'

class Cadastro(models.Model):
    nome = models.CharField(max_length=50)
    nasc = models.CharField(max_length=50)
    cpf = models.IntegerField()
    telefone = models.CharField(max_length=15, default='00.00000.0000')
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, null=True)  
    email = models.CharField(max_length=50)
    senha = models.CharField(max_length=50)
    
    def __str__(self):
        return f'{self.nome} - {self.telefone} - R$ {self.saldo}'
    
    

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

    conta_cliente = models.ForeignKey(Cliente, null=True, verbose_name='Cliente', related_name='transacoes',on_delete=models.PROTECT)
    descricao = models.CharField(max_length=120, null=False)
    valor = models.FloatField(null=False)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.conta_cliente


class Contas(models.Model):
    agencia = models.CharField(max_length=10)
    # cliente = models.OneToOneField('Cliente', on_delete=models.CASCADE)
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
    
    
class Saque(models.Model):
    conta = models.ForeignKey('Contas', on_delete=models.CASCADE)
    valor = models.DecimalField(decimal_places=2, max_digits=10, default=0.00)
    data_saque = models.DateTimeField(auto_now_add=True)
    
    def get_data_saque(self):
        return self.data_saque.strftime('%d/%m/%Y %H:%M')
    
@receiver(post_save, sender=Deposito)
def update_saldo(sender, instance, **kwargs):
    instance.conta.saldo += instance.valor
    instance.conta.save()
    
@receiver(post_save, sender=Saque)
def update_saldo(sender, instance, **kwargs):
    instance.conta.saldo -= instance.valor
    instance.conta.save()
        
    