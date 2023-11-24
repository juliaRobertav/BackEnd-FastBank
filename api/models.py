from django.db import models

# Create your models here.

class Cadastro(models.Model):
    nome = models.CharField(max_length=50)
    nasc = models.CharField(max_length=50)
    cpf = models.IntegerField()
    email = models.CharField(max_length=50)
    senha = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome
    
    

class Cliente(models.Model):
    
    def upload_imagem_cliente(instance, filename):
        return f"{instance.conta}-{filename}"

    nome = models.CharField(max_length=120)
    conta = models.CharField(max_length=10, unique=True)
    limite = models.FloatField(null=True)
    saldo =  models.FloatField(null=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now_add=True)
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
