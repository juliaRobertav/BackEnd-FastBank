from rest_framework import viewsets
from .models import Cadastro, Cliente, Transacao, Deposito, Saque, Emprestimo, Credito, Login
from .serializers import CadastroSerializer, ClienteSerializer, TransacaoSerializer, DepositoSerializer, SaqueSerializer, EmprestimoSerializer, CreditoSerializer, LoginSerializer
from rest_framework.response import Response
from decimal import Decimal
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters


class HomeView(APIView):
      permission_classes = (IsAuthenticated, )
      
      def get(self, request):
            content = {'message': 'Token gerado com sucesso!'}
            
            return Response(content)
      
      
class LogoutView(APIView):
      permission_classes = (IsAuthenticated, )
      def post(self, request):
            try:
                  refresh_token = request.data["refresh_token"]
                  token = RefreshToken(refresh_token)
                  token.blacklist()
                  return Response(status=status.HTTP_205_RESET_CONTENT)
            except Exception as e:
                  return Response(status=status.HTTP_400_BAD_REQUEST)
      

class CadastroViewSet(viewsets.ModelViewSet):
    queryset = Cadastro.objects.all()
    serializer_class = CadastroSerializer
    

    
class LoginViewSet(viewsets.ModelViewSet):
      
      serializer_class = LoginSerializer
      queryset = Login.objects.all()
      
      def create(self, request, *args, **kwargs):  
            
            serializer = self.serializer_class(data=request.data)
            
            try:
                  if serializer.is_valid():
                        email_cliente = serializer.validated_data.get('email')
                        senha_cliente = serializer.validated_data.get('senha')
                        logado_cliente = serializer.validated_data.get('logado')
                        
                        dados_cliente = Cadastro.objects.filter(email=email_cliente).first()
            
                        if dados_cliente:
                              
                              senha_correta = check_password(password=senha_cliente, encoded=dados_cliente.senha)
                              
                              if email_cliente == dados_cliente.email and senha_correta and dados_cliente.tentativas < 3:
                                    dados_cliente.tentativas = 0
                                    dados_cliente.save()
                                    return Response(data={"id": dados_cliente.id, "nome": dados_cliente.nome}, status=200)
                              elif dados_cliente.tentativas > 3 :
                                    dados_cliente.tentativas = 0
                                    dados_cliente.save()
                                    return Response(data={"Bloqueado...": "Tentativas ultrapassadas."}, status=403)
                              
                              else:
                                    dados_cliente.tentativas = dados_cliente.tentativas + 1
                                    dados_cliente.save()
                                    return Response({"Erro": "Dados inválidos"}, status=401)
                        else:
                              return Response({"Erro!": "Cliente não encontrado..."}, status=404)
                  else:
                        return Response(data=serializer.errors, status=400)
            except Cadastro.DoesNotExist:
                  return Response({"Erro": "Cliente não cadastrado"}, status=404)
            except Exception as e:
                  return Response({"Erro": str(e)}, status=500)
                        

   
      
    
class ClienteViewSet(viewsets.ModelViewSet):
      # permission_classes = (IsAuthenticated, )
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
      permission_classes = (IsAuthenticated, )
      serializer_class = TransacaoSerializer
      queryset = Transacao.objects.all()
    # permission_classes = (IsAuthenticated,)

      def create(self, request, *args, **kwargs):
            dados_da_transacao = request.data #pega todos os dados informados na API e armazena em dados _da_transacao
            valor_da_transacao = Decimal(dados_da_transacao['valor']) #buscando um dado especifico
            numero_da_conta = dados_da_transacao['conta_cliente']
            cliente_conta = Cliente.objects.filter(conta=numero_da_conta).values("saldo")
            saldo = cliente_conta[0]
            saldo = saldo['saldo']

            if  valor_da_transacao < 0 : 
                  return Response(status=403, data='Valor da transação menor que zero')

                #verifica se tem saldo para a transação
            if saldo < (valor_da_transacao * -1): # Multiplicado por -1 para inverter o valor informado e comparar com o saldo disponivel do cliente

                  return Response(status=403, data='Não há saldo suficiente para realizar esta transação. ')

            # atualiza saldo da conta e grava transacao na sequencia
            _serializer = self.serializer_class(data=request.data)
            if _serializer.is_valid():

               # atualiza saldo da conta
               cliente_conta = Cliente.objects.get(conta=numero_da_conta)
               cliente_conta.saldo = saldo + valor_da_transacao  
               cliente_conta.save()
               # registra a transação
               _serializer.save()
               return Response(data=_serializer.data, status=201)
      

      
class DepositoViewSet(viewsets.ModelViewSet):
      permission_classes = (IsAuthenticated, )
      queryset = Deposito.objects.all()
      serializer_class = DepositoSerializer
      
      
class SaqueViewSet(viewsets.ModelViewSet):
      permission_classes = (IsAuthenticated, )
      queryset = Saque.objects.all()
      serializer_class = SaqueSerializer
      


class EmprestimoViewSet(viewsets.ModelViewSet): # ainda não ta funfando
      # permission_classes = (IsAuthenticated, )
      queryset = Emprestimo.objects.all()
      serializer_class = EmprestimoSerializer
    
      filter_backends = [filters.SearchFilter]
      search_fields = ['cliente', 'id', 'parcelas', 'valor_parcela']

      def create(self, request, *args, **kwargs):
            dados_do_emprestimo = request.data.dict()
            cliente_emprestimo = dados_do_emprestimo['cliente']
            valor_do_emprestimo = Decimal(dados_do_emprestimo['valor']) 
            parcelas_emprestimo = int(dados_do_emprestimo['parcelas'])
            
            try:
                  cliente = Cliente.objects.get(id=cliente_emprestimo)
                  
                  
                  if valor_do_emprestimo > 20000:
                        return Response({"Negado": "Ultrapassou limite máximo de R$20.000,00"}, status=401)
                  
                  if parcelas_emprestimo == 0:
                        return Response({"Erro": "Número de parcelas não pode ser zero"}, status=400)

                  valor_parcela = valor_do_emprestimo / parcelas_emprestimo
                  valor_parcela = round(valor_parcela, 2)
                  dados_modificados = dados_do_emprestimo.copy()  # Cria uma cópia mutável
                  dados_modificados['valor_parcela'] = Decimal(valor_parcela)
                  
                  serializer = self.serializer_class(data=request.data)
                  if serializer.is_valid():
                        cliente.saldo = cliente.saldo + valor_do_emprestimo
                        cliente.save()
                        serializer.save()
                        return Response({"Aprovado": f"O valor da sua parcela é {valor_parcela}"}, status=200)
                  else:
                        return Response(data=serializer.errors, status=400)
                  
            except Cliente.DoesNotExist:
                  return Response({"Erro": "Cliente não cadastrado"}, status=404)
            except Exception as e:
                  return Response({"Erro": str(e)}, status=500)
           


class CreditoViewSet(viewsets.ModelViewSet):
      # permission_classes = (IsAuthenticated, )
      queryset = Credito.objects.all()
      serializer_class = CreditoSerializer
      
      filter_backends = [filters.SearchFilter]
      search_fields = ['cliente', 'limite', 'cvv']
    
      def create(self, request, *args, **kwargs):
        
            limite_cliente = Decimal(request.data['limite'])
            dados_do_cliente = request.data['cliente']
        
            try:
              cliente = Cliente.objects.get(id=dados_do_cliente)
              
              if limite_cliente > 1000:
                  return Response({"Recusado": "O limite ultrapassou R$1.000,00"}, status=400)
              
              serializer = self.serializer_class(data=request.data)
              if serializer.is_valid():
                  cliente.cartao_credito = True
                  serializer.save()
                    
                  return Response({"Sucesso": "Cartão Aprovado"}, status=200)
              else:
                  return Response(data=serializer.errors, status=400)
            
            except Cliente.DoesNotExist:
                  return Response({"Erro": "Cliente não cadastrado"}, status=404)
            except Exception as e:
                  return Response({"Erro": str(e)}, status=500)




