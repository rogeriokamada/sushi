from django.http import HttpResponse
from django.views.generic import ListView
from django.shortcuts import render
from produto.models import Produto,Categoria
from django.db.models import Count
# Create your views here.



def home(request):
    
    categorias = Categoria.objects.filter(ativo=True).annotate(num_produtos=Count('produto')).exclude(num_produtos=0)
    produtos = Produto.objects.filter(destaque=True,ativo=True)
    return render(request,'index.html', {'produtos':produtos ,'categorias':categorias})


def produto_list(request, id):
    categorias = Categoria.objects.filter(ativo=True).annotate(num_produtos=Count('produto')).exclude(num_produtos=0)
    produtos = Produto.objects.filter(categoria=id)
    #produtos = Produto.objects
    return render(request,'produto/produto_list.html', {'produtos':produtos,'categorias':categorias })

