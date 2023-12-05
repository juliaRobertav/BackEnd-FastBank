from rest_framework import viewsets
from .models import Cadastro, Cliente, Transacao, Deposito, Saque, Emprestimo, Credito, Login
from .serializers import CadastroSerializer, ClienteSerializer, TransacaoSerializer, DepositoSerializer, SaqueSerializer, EmprestimoSerializer, CreditoSerializer, LoginSerializer
from rest_framework.response import Response
from decimal import Decimal
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password


# terminar:
#  https://medium.com/@ronakchitlangya1997/jwt-authentication-with-react-js-and-django-c034aae1e60d

class HomeView(APIView):
      permission_classes = (IsAuthenticated, )
      
      def get(self, request):
            content = {'message': 'Token gerado com sucesso!'}
            
            return Response(content)
      
      
# class LogoutView(APIView):
#       permission_classes = (IsAuthenticated, )
#       def post(self, request):
#             try:
#                   refresh_token = request.data["refresh_token"]
#                   token = RefreshToken(refresh_token)
      

class CadastroViewSet(viewsets.ModelViewSet):
    queryset = Cadastro.objects.all()
    serializer_class = CadastroSerializer
    

    
class LoginViewSet(viewsets.ModelViewSet):
      
      serializer_class = LoginSerializer
      queryset = Login.objects.all()
      
      def create(self, request, *args, **kwargs):  
            email_cliente = request.data.get('email')
            senha_cliente = request.data.get('senha')
            
            dados_cliente = Cadastro.objects.filter(email=email_cliente).first()
            
            if dados_cliente:
                  
                  senha_correta = check_password(password=senha_cliente, encoded=dados_cliente.senha)
                  if email_cliente == dados_cliente.email and senha_cliente == dados_cliente.senha and dados_cliente.tentativas < 3:
                        dados_cliente.tentativas = 0
                        return Response(data={"id": dados_cliente.id, "nome": dados_cliente.nome}, status=200)
                  elif dados_cliente.tentativas > 3 :
                        dados_cliente.tentativas = 0
                        return Response(data={"Bloqueado...": "Tentativas ultrapassadas."}, status=403)
                  
                  else:
                        dados_cliente.tentativas = dados_cliente.tentativas + 1
                        return Response({"Erro": "Dados inválidos"}, status=401)
            else:
                  return Response({"Erro!"}, status=400)
                        

   
      
    
class ClienteViewSet(viewsets.ModelViewSet):
      serializer_class = ClienteSerializer
      queryset = Cliente.objects.all()


      def create(self, request, *args, **kwargs):
            dados_do_cliente = request.data #pega todos os dados informados na APi e armazena em dados _do cliente
            limite = float(dados_do_cliente['limite'])
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
            valor_da_transacao = Decimal(dados_da_transacao['valor']) #buscando um dado especifico
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
      

      
class DepositoViewSet(viewsets.ModelViewSet):
      queryset = Deposito.objects.all()
      serializer_class = DepositoSerializer
      
      
class SaqueViewSet(viewsets.ModelViewSet):
      queryset = Saque.objects.all()
      serializer_class = SaqueSerializer
      


class EmprestimoViewSet(viewsets.ModelViewSet):
    queryset = Emprestimo.objects.all()
    serializer_class = EmprestimoSerializer

    def create(self, request, *args, **kwargs):
            dados_do_emprestimo = request.data 
            valor_do_emprestimo = Decimal(dados_do_emprestimo['valor']) 
            numero_da_conta = dados_do_emprestimo['conta']
            cliente_conta = Cliente.objects.filter(conta=numero_da_conta).values("saldo")
            
            saldo = cliente_conta[0]
            saldo = saldo['saldo']
   
            if  valor_do_emprestimo < 0 : 
                  return Response(status=403, data='Valor do empréstimo menor que zero')

            if saldo < valor_do_emprestimo : 

                  return Response(status=403, data='Não há saldo suficiente para realizar esta transação. ')

    
            _serializer = self.serializer_class(data=request.data)
 
            if _serializer.is_valid():

               cliente_conta = Cliente.objects.get(conta=numero_da_conta)
               cliente_conta.saldo = saldo + valor_do_emprestimo 
               cliente_conta.save()

               _serializer.save()
               return Response(data=_serializer.data, status=201)

    


class CreditoViewSet(viewsets.ModelViewSet):
      queryset = Credito.objects.all()
      serializer_class = CreditoSerializer
    
      def create(self, request, *args, **kwargs):
        dados_do_credito = request.data

        numero_da_conta = dados_do_credito['cliente']

        try:
            conta = Cliente.objects.get(conta=numero_da_conta)
        except Cliente.DoesNotExist:
            return Response(status=404, data='Cliente não encontrado')

        renda = conta.renda
  
        if renda >= 1000:
            return Response(status=201, data='Cartão Aprovado!')
        elif renda < 1000:
              return Response(status=403, data='Cartão de crédito não aprovado...')
        else:
            return Response(status=403, data='Algo deu errado...')
    


