from rest_framework import serializers
from .models import Cadastro, Cliente, Transacao, Contas, Deposito, Saque, Emprestimo, Credito


class CadastroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cadastro
        fields = ('id', 'nome', 'nasc', 'cpf', 'email', 'senha')
        
        

class ClienteSerializer(serializers.ModelSerializer):

      class Meta:  # Classe interna
            model = Cliente
            fields = '__all__'
            
            
            
class TransacaoSerializer(serializers.ModelSerializer):

    conta_cliente = serializers.CharField()

    class Meta:  # Classe interna
        model = Transacao
        fields = '__all__'

    def create(self, validated_data):
        conta_cli = validated_data.pop('conta_cliente')
        cliente_instance, created = Cliente.objects.get_or_create(conta=conta_cli)
        transacao_instance = Transacao.objects.create(**validated_data, conta_cliente=cliente_instance)
        return transacao_instance

#Validações de entrada nos campos podem ser consultadas em Validators
# https://django-rest-framework.org/api-guide/validators/


class ContaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contas
        fields = ['agencia', 'conta', 'saldo', 'get_ultima_movimentacao']
        

# class SaldoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cliente
#         fields = ['cliente', 'saldo', 'ultima_movimentacao']
        
        
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

