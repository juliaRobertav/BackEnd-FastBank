from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password

# Create your models here.

    
    

class Cadastro(models.Model):
    
    def upload_imagem_cliente(instance, filename):
        return f"{instance.nome}-{filename}"
    
    nome = models.CharField(max_length=50)
    nasc = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=50)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=50)
    cep = models.CharField(max_length=10)
    imagem = models.ImageField(upload_to=upload_imagem_cliente, blank=True, null=True)
    tentativas = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.senha.startswith('pbkdf2_sha256$') and not self.senha.startswith('bcrypt$'):
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.nome} - {self.email}- {self.senha}'
    
 
class Login(models.Model):
    email = models.EmailField(unique=True)
    senha =  senha = models.CharField(max_length=50)
    
# modelo criado para o Cliente colocar informações adicionais de cadastro
class Cliente(models.Model):
    

    cliente = models.ForeignKey(Cadastro, null=True, verbose_name='nome_cliente', on_delete=models.PROTECT)
    conta = models.CharField(max_length=10, unique=True)
    limite = models.FloatField(null=True)
    ultima_movimentacao = models.DateTimeField(auto_now_add=True)
    renda = models.FloatField()
    agencia = models.CharField(max_length=10)
    saldo = models.DecimalField(decimal_places=2, max_digits=30, default=0.00)

    def __str__(self):
        return self.conta
    
    
    
class Transacao(models.Model):

    conta_cliente = models.ForeignKey(Cliente, null=True, verbose_name='Cliente', related_name='transacoes',on_delete=models.PROTECT)
    descricao = models.CharField(max_length=120, null=False)
    valor = models.IntegerField(null=False)
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.conta_cliente



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
        
        
 # faltar aprovar       
class Emprestimo(models.Model):
    cliente = models.ForeignKey('Cadastro', on_delete=models.CASCADE)
    conta = models.OneToOneField('Cliente', on_delete=models.CASCADE, default='')
    valor = models.FloatField()
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Empréstimo de {self.valor} para {self.cliente}'
    
  # falta aprovar 
class Credito(models.Model):
    cliente = models.ForeignKey(Cadastro, null=True, verbose_name='nome_cliente', on_delete=models.PROTECT)
    renda = models.OneToOneField(Cliente,  null=True, verbose_name='renda_cliente', related_name='credito',on_delete=models.PROTECT)
    
    def __str__(self):
        return self.cliente
