from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

from api.views import CadastroViewSet, ClienteViewSet, TransacaoViewSet, DepositoViewSet, SaqueViewSet, EmprestimoViewSet, CreditoViewSet, HomeView, LoginViewSet

from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings

router = routers.DefaultRouter()
router.register(r'api_cadastro', CadastroViewSet, basename="cadastro")
router.register(r'api_login', LoginViewSet, basename="login")
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
    
    path('home/', HomeView.as_view(), name='home'),
    
    path('api_transacao/<int:pk>', TransacaoViewSet.as_view({'get':'transacaoId'}), name="transacaoId"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)