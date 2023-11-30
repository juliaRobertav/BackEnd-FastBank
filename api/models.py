from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.

#TESTAR: 

# class Endereco(models.Model):
#     rua = models.CharField(max_length=100)
#     numero = models.CharField(max_length=10)
#     cidade = models.CharField(max_length=50)
#     estado = models.CharField(max_length=50)
#     cep = models.CharField(max_length=10)

#     def __str__(self):
#         return f'{self.rua}, {self.numero} - {self.cidade}/{self.estado} - CEP: {self.cep}'
    
    
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

    # rg = models.CharField(max_length=20, default='')
    # telefone = models.CharField(max_length=15, default='00.00000.0000')
    # endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE, null=True)  
    
    

class Cadastro(models.Model):
    
    def upload_imagem_cliente(instance, filename):
        return f"{instance.nome}-{filename}"
    
    nome = models.CharField(max_length=50)
    nasc = models.DateField()
    cpf = models.IntegerField()
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=50)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=10)
    imagem = models.ImageField(upload_to=upload_imagem_cliente, blank=True, null=True)
    
    def __str__(self):
        return f'{self.nome} - {self.email}- {self.senha}'
    
 
class Login(models.Model):
    
    email = models.ForeignKey(Cadastro, on_delete=models.CASCADE, related_name='logins_email')
    senha = models.OneToOneField(Cadastro, on_delete=models.CASCADE, related_name='login_senha')
    
    
class Cliente(models.Model):
    
    # def upload_imagem_cliente(instance, filename):
    #     return f"{instance.conta}-{filename}"

    cliente = models.ForeignKey(Cadastro, null=True, verbose_name='nome_cliente', on_delete=models.PROTECT)
    conta = models.CharField(max_length=10, unique=True)
    limite = models.FloatField(null=True)
    # criado_em = models.DateTimeField(auto_now_add=True)
    ultima_movimentacao = models.DateTimeField(auto_now_add=True)
    renda = models.FloatField()
    agencia = models.CharField(max_length=10)
    saldo = models.DecimalField(decimal_places=2, max_digits=30, default=0.00)
    # imagem = models.ImageField(upload_to=upload_imagem_cliente, blank=True, null=True)

    def __str__(self):
        return self.conta
    
    
    
class Transacao(models.Model):

    conta_cliente = models.ForeignKey(Cliente, null=True, verbose_name='Cliente', related_name='transacoes',on_delete=models.PROTECT)
    descricao = models.CharField(max_length=120, null=False)
    valor = models.FloatField(null=False)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.conta_cliente


# class Contas(models.Model):
    
#     cliente = models.ForeignKey(Cliente, null=True, verbose_name='Cliente', related_name='Contas', on_delete=models.PROTECT)
#     agencia = models.CharField(max_length=10)
#     conta = models.OneToOneField(Cliente, null=True, verbose_name='conta_cliente', on_delete=models.CASCADE)
#     saldo = models.DecimalField(decimal_places=2, max_digits=30, default=0.00)
#     ultima_movimentacao = models.DateTimeField(auto_now=True)
    
#     def __str__(self) :
#         return f'{str(self.agencia)}/{str(self.conta)}/{str(self.saldo)}'
    
#     def get_ultima_movimentacao(self):
#         return self.ultima_movimentacao.strftime('%d/%m/%Y %H:%M')
    
    # def get_saldo(self):
    #     return self.saldo
    
    
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
    conta = models.ForeignKey('Cliente', on_delete=models.CASCADE)
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
        
        
        
class Emprestimo(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    valor = models.FloatField()
    taxa_juros = models.FloatField()
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Empréstimo de {self.valor} para {self.cliente}'
    
    
class Credito(models.Model):
    cliente = models.ForeignKey(Cadastro, null=True, verbose_name='nome_cliente', on_delete=models.PROTECT)
    renda = models.OneToOneField(Cliente,  null=True, verbose_name='renda_cliente', related_name='credito',on_delete=models.PROTECT)
    
    def __str__(self):
        return self.cliente
