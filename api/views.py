from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import Cadastro, Cliente, Transacao, Deposito, Saque, Emprestimo, Credito, Login
from .serializers import CadastroSerializer, ClienteSerializer, TransacaoSerializer, DepositoSerializer, SaqueSerializer, EmprestimoSerializer, CreditoSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


# class EnderecoViewSet(viewsets.ModelViewSet):
#       queryset = Endereco.objects.all()
#       serializer_class = EnderecoSerializer
      

class CadastroViewSet(viewsets.ModelViewSet):
    queryset = Cadastro.objects.all()
    serializer_class = CadastroSerializer
    
    
class LoginViewSet(viewsets.ModelViewSet):
      
      serializer_class = LoginSerializer
      queryset = Login.objects.all()
      
      def create(self, request, *args, **kwargs):  # Use "create" em vez de "post"
            email = request.data.get('email')
            senha = request.data.get('senha')

        # Autenticar o usuário
            user = authenticate(email=email, senha=senha)

            if user:
            # Criar ou obter token de autenticação
                  token, created = Token.objects.get_or_create(user=user)

            # Serializar os dados, incluindo detalhes do Cadastro
                  login_serializer = LoginSerializer(user.login)
                  response_data = {
                  'token': token.key,
                  'login_details': login_serializer.data
                  }

                  return Response(response_data, status=status.HTTP_200_OK)
      
            else:
                  
                  return Response({'error': 'Credenciais inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
      
    
class ClienteViewSet(viewsets.ModelViewSet):
      serializer_class = ClienteSerializer
      queryset = Cliente.objects.all()
    # permission_classes = (IsAuthenticated,)

      def create(self, request, *args, **kwargs):
            dados_do_cliente = request.data #pega todos os dados informados na APi e armazena em dados _do cliente
            limite = float(dados_do_cliente['limite'])
            # Exemplo de regra de negócio: Valor máximo do limite = R$ 1000,00
            if  limite > 1000:
                  return Response(status=403, data='O valor máximo permitido para limite em conta corrente é R$ 1000,00 ')

            _serializer = self.serializer_class(data=request.data)
            if _serializer.is_valid():
               _serializer.save()
               return Response(data=_serializer.data, status=201)
           
           
class TransacaoViewSet(viewsets.ModelViewSet):
      serializer_class = TransacaoSerializer
      queryset = Transacao.objects.all()
    # permission_classes = (IsAuthenticated,)

      def create(self, request, *args, **kwargs):
            dados_da_transacao = request.data #pega todos os dados informados na API e armazena em dados _da_transacao
            valor_da_transacao = float(dados_da_transacao['valor']) #buscando um dado especifico
            numero_da_conta = dados_da_transacao['conta_cliente']
            cliente_conta = Cliente.objects.filter(conta=numero_da_conta).values("saldo")
            # O Resultado da consulta acima retorna um queryset assimm <QuerySet [{'saldo': 300}]>
            # Para lermos no código aqui da função devemos fatiá-lo(slice)
            # Primeiro acessamos o índice da lista passando [0]
            # o resultado será {'saldo': 300}
            # feito isso, faço a recuperação apenas do valor passando o campo que desejo o valor, no caso ['saldo']
            saldo = cliente_conta[0]
            saldo = saldo['saldo']
            #verifica se é débito ou crédito pelo valor.
            # se receber um valor positivo será um crédito na conta e não precisa fazer nada alem de creditar
            # se receber valor negativo é para fazer um débito da conta e portanto deve verificar se tem saldo suficiente
            # print("Valor da transação ", valor_da_transacao)
            if  valor_da_transacao < 0 : # significa que será um débito da conta para pagamento de um boleto por exemplo
            #     print("Valor da transação menor que Zero", valor_da_transacao)
                  return Response(status=403, data='Valor da transação menor que zero')

                #verifica se tem saldo para a transação
            if saldo < (valor_da_transacao * -1): # Multiplicado por -1 para inverter o valor informado e comparar com o saldo disponivel do cliente

                  return Response(status=403, data='Não há saldo suficiente para realizar esta transação. ')

            # atualiza saldo da conta e grava transacao na sequencia
            _serializer = self.serializer_class(data=request.data)
            #print("serializer preenchido", _serializer)
            if _serializer.is_valid():
               #print("serializer validado")
               # atualiza saldo da conta
               cliente_conta = Cliente.objects.get(conta=numero_da_conta)
               cliente_conta.saldo = saldo + valor_da_transacao  # o 'valor' deve acompanhar o valor negativo de débito
               cliente_conta.save()
               # # registra a transação
               _serializer.save()
               return Response(data=_serializer.data, status=201)


# class ContasViewSet(viewsets.ModelViewSet):
#       queryset = Contas.objects.all()
#       serializer_class = ContaSerializer
      
      
# class SaldoList(ListAPIView):
#       queryset = Cliente.objects.all()
#       serializer_class = SaldoSerializer
      
class DepositoViewSet(viewsets.ModelViewSet):
      queryset = Deposito.objects.all()
      serializer_class = DepositoSerializer
      
      
class SaqueViewSet(viewsets.ModelViewSet):
      queryset = Saque.objects.all()
      serializer_class = SaqueSerializer
      
      
class EmprestimoViewSet(viewsets.ModelViewSet):
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer
    
    #FALTA TERMINAR (LÓGICA) EMPRESTIMO:
#     def create(self, request, *args, **kwargs):
#       dados_do_emprestimo = request.data #pega todos os dados informados na API e armazena em dados _da_transacao
#       valor_do_emprestimo = float(dados_do_emprestimo['valor']) #buscando um dado especifico
#       numero_da_conta = dados_do_emprestimo['conta_cliente']
#       cliente_conta = Cliente.objects.filter(conta=numero_da_conta).values("saldo")
#       return super().create(request, *args, **kwargs)
# adicionar nascimento para validar se é de maior!

class CreditoViewSet(viewsets.ModelViewSet):
    queryset = Credito.objects.all()
    serializer_class = CreditoSerializer
    


