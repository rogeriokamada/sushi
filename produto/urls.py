from django.urls import path
from . import views

app_name = 'produto'
urlpatterns = [

    path('', views.home, name="home"),
    path('categoria/<int:id>', views.produto_list, name="produto_list")
    
]
