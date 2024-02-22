from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'base'
urlpatterns = [
    path('', views.base, name='base'),
    path('<int:agent_id>/', views.profile, name = 'profile'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_request, name = 'logout'),
    path('login/', views.login_request, name= 'login'),
    path('<int:agent_id>/verification', views.verification_request, name='verification'),
    path('<int:agent_id>/verification/pending/<int:verification_id>/', views.verification_pending, name='pending'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)