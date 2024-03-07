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
    path('policies/', views.policies, name='policies'),
    path('leave-a-message/', views.leaveamessage, name='lam'),
    path('add_banks/', views.load_banks, name='add_bank'),
    path('process-bank', views.add_bank, name='pending_bank'),
    path('validation/', views.pending_bank, name='validating'),
    path('depo/', views.depo, name='depo'),
    path('messages/', views.messages, name = 'messages'),
    path('messages/<int:message_id>/', views.message, name='message'),
    path('transactions/', views.transac, name='trans'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)