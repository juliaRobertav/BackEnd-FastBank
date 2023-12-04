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
from rest_framework_simplejwt import views as jwt_views

from api.views import CadastroViewSet, ClienteViewSet, TransacaoViewSet, DepositoViewSet, SaqueViewSet, EmprestimoViewSet, CreditoViewSet, HomeView

from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'api_cadastro', CadastroViewSet, basename="cadastro")
# router.register(r'api_login', LoginViewSet, basename="login")
router.register(r'api_cliente', ClienteViewSet, basename="cliente")
router.register(r'api_transacao', TransacaoViewSet, basename="transacao")
router.register(r'api_deposito', DepositoViewSet, basename="deposito")
router.register(r'api_saque', SaqueViewSet, basename="saque")
router.register(r'api_emprestimo', EmprestimoViewSet, basename="emprestimo")
router.register(r'api_credito', CreditoViewSet, basename="credito")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('app-auth/', include('rest_framework.urls')),
    
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'), 
    
    path('home/', HomeView.as_view(), name='home')
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)