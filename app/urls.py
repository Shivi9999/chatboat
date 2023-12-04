from django.urls import path
from . import views
urlpatterns = [
    path('get_answer/', views.get_answer, name='get_answer'),
    #path('', views.index, name='index'),
    path('', views.chat, name='chatbot_page'),
    
]
