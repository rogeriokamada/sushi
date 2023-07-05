from django.urls import path
from . import views

app_name = 'produto'
urlpatterns = [

    path('', views.home, name="home"),
    path('categoria/<slug:slug>', views.produto_list, name="produto_list"),
    path('carrinho/adicionar/<int:produto_id>/', views.adicionar_item_carrinho, name='adicionar_item_carrinho'),
    #path('carrinho/remover/<int:item_id>/', views.remover_item_carrinho, name='remover_item_carrinho'),
    path('carrinho/remover/<int:item_id>/', views.remover_item_carrinho, name='remover_item_carrinho'),

    #path('carrinho/', views.visualizar_carrinho, name='visualizar_carrinho'),
    path('carrinho/atualizar_quantidade/<int:item_id>/', views.atualizar_quantidade, name='atualizar_quantidade'),


    path('enviar_pedido/<str:tipo>', views.enviar_mensagem_whatsapp, name='enviar_mensagem_whatsapp'),
     
]



