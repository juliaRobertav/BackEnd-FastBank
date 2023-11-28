"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
<<<<<<< HEAD
from api.views import CadastroViewSet, ClienteViewSet, TransacaoViewSet, ContasViewSet, DepositoViewSet, SaqueViewSet, EmprestimoViewSet, CreditoViewSet
=======
from api.views import CadastroViewSet, ClienteViewSet, TransacaoViewSet, ContasViewSet, DepositoViewSet, SaqueViewSet, EmprestimoViewSet
>>>>>>> ae24f884adee08ad6dc7c9b4f6ed028f167eae77
from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'cadastro', CadastroViewSet)
router.register(r'api_cliente', ClienteViewSet, basename="cliente")
router.register(r'api_transacao', TransacaoViewSet, basename="transacao")
router.register(r'api_contas', ContasViewSet, basename="conta")
router.register(r'api_deposito', DepositoViewSet, basename="deposito")
router.register(r'api_saque', SaqueViewSet, basename="saque")
router.register(r'api_emprestimo', EmprestimoViewSet, basename="emprestimo-teste")
<<<<<<< HEAD
router.register(r'api_credito', CreditoViewSet, basename="credito-teste")
=======
# router.register(r'api_credito', CreditoViewSet, basename="credito-teste")
>>>>>>> ae24f884adee08ad6dc7c9b4f6ed028f167eae77
# router.register(r'api_saldo', SaldoList.as_view(), basename="saldo-teste")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('app-auth/', include('rest_framework.urls')),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)