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
      permission_classes = (IsAuthenticated, )
      queryset = Cadastro.objects.all()
      serializer_class = CadastroSerializer
    

    
class LoginViewSet(viewsets.ModelViewSet):
      permission_classes = (IsAuthenticated, )
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
      permission_classes = (IsAuthenticated, )
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
      permission_classes = (IsAuthenticated,)
      serializer_class = TransacaoSerializer
      queryset = Transacao.objects.all()

      def create(self, request, *args, **kwargs):
            dados_recebidos = request.data # recebendo os dados para fazer a transferencia
            valor_enviado = Decimal(dados_recebidos['valor'])
            cliente_enviando = dados_recebidos['conta_enviando'] 
            cliente_recebendo = dados_recebidos['conta_recebendo']

            try:
                  dados_cliente_env = Cliente.objects.get(cliente=cliente_enviando) # consultando no banco se o cliente que esta enviando, existe
                  dados_cliente_rec = Cliente.objects.get(conta=cliente_recebendo) # consultando no banco se o cliente que esta recebendo, existe

                  if valor_enviado > dados_cliente_env.saldo: #verificando se existe saldo suficiente
                       return Response({"Mensage": "Transação negada por falta de saldo."}, status=400)
                  
                  _serializer_env = self.serializer_class(data=request.data) #serializando

                  if _serializer_env.is_valid():
                       dados_cliente_env.saldo -= valor_enviado #alterando o valor do saldo
                       dados_cliente_env.save() #salvando a alteracao do saldo

                       dados_cliente_rec.saldo += valor_enviado #alterando o valor do saldo
                       dados_cliente_rec.save() #salvando a alteracao do saldo

                       _serializer_env.save() # SALVANDO A TRANSAÇÃO
                       return Response({"Mensage":"Transação realizada com sucesso!"}, status=200)
                  else:
                       return Response(data=_serializer_env.errors, status=405) # retorna erro de validação
            except Cliente.DoesNotExist:
                  return Response({"Mensagem": "Clientes não encontrados"}, status=404)
            except Exception as e:
                  return Response({"Erro:": str(e)}, status=500)  
            
      def retrieve(self, request, pk=None):
            try:
                 info = Cliente.objects.get(cliente=pk) #puxando as informações do cliente

                 transacoes = Transacao.objects.filter(conta_enviando=pk) #puxando os enviados
                 transacoes2 = Transacao.objects.filter(conta_recebendo=info.conta) #puxando os recebidos

            #      serializer = TransacaoSerializer(transacoes, many=True)
            #      serializer2 = TransacaoSerializer(transacoes2, many=True)
                 
                 todas_transacoes = list(transacoes) + list(transacoes2)
                 serializer = TransacaoSerializer(todas_transacoes, many=True)
                 return Response(serializer.data, status=200)
            except Transacao.DoesNotExist:
                 return Response({"Mensagem": "Transações não encontradas"}, status=404)
            
            except Exception as e: #caso haja outro erro
                  return Response({"Erro:": str(e)}, status=500) #retorna o erro encontrado

transacaoId = TransacaoViewSet.as_view({'get': 'transacaoId'}, lookup_url_kwarg='pk')
      

      
class DepositoViewSet(viewsets.ModelViewSet):
      permission_classes = (IsAuthenticated, )
      queryset = Deposito.objects.all()
      serializer_class = DepositoSerializer
      
      
class SaqueViewSet(viewsets.ModelViewSet):
      permission_classes = (IsAuthenticated, )
      queryset = Saque.objects.all()
      serializer_class = SaqueSerializer
      


class EmprestimoViewSet(viewsets.ModelViewSet):
      permission_classes = (IsAuthenticated, )
      queryset = Emprestimo.objects.all()
      serializer_class = EmprestimoSerializer
    
      filter_backends = [filters.SearchFilter]
      search_fields = ['cliente', 'id', 'parcelas', 'valor_parcela']

      def create(self, request, *args, **kwargs):
            dados_do_emprestimo = request.data
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
      permission_classes = (IsAuthenticated, )
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



