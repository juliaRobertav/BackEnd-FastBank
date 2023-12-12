from rest_framework import serializers
from .models import Cadastro, Cliente, Transacao, Deposito, Saque, Emprestimo, Credito, Login, Saldo
from django.contrib.auth import authenticate


        

class CadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cadastro
        fields = '__all__'

        
        
        
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):

      class Meta:  # Classe interna
            model = Cliente
            fields = '__all__'
            

class SaldoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saldo
        fields = '__all__'
            
class TransacaoSerializer(serializers.ModelSerializer):

    class Meta:  # Classe interna
        model = Transacao
        fields = '__all__'


        
        
class DepositoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposito
        fields = ['id', 'conta', 'valor', 'get_data_deposito']
        
        
class SaqueSerializer(serializers.ModelSerializer):
    class Meta:
        model =Saque
        fields = ['id', 'conta', 'valor', 'get_data_saque']
        
        
class EmprestimoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emprestimo
        fields = '__all__'
        
        

class CreditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credito
        fields = '__all__'
