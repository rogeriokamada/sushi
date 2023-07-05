from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404, redirect
from produto.models import Produto,Categoria,Carrinho, ItemCarrinho
from django.db.models import Count
from urllib.parse import urlencode
from django.urls import reverse
from django.db.models import Sum
from django.db.models import Q

def home(request):

    categorias = Categoria.objects.filter(Q(ativo=True) | Q(nome='destaque')).annotate(num_produtos=Count('produto')).order_by('order')

    #categorias = Categoria.objects.filter(ativo=True).annotate(num_produtos=Count('produto')).exclude(num_produtos=0)
    produtos = Produto.objects.filter(ativo=True)
    destaque = Produto.objects.filter(ativo=True, destaque=True)

    # Verifique se o carrinho existe ou crie um novo carrinho
    carrinho, created = Carrinho.objects.get_or_create()
    # Obtenha todos os itens do carrinho


    item_removido = request.GET.get('item_removido', False)
    if request.method == 'POST': 
        #produto = int(request.POST.get('produto_id'))
        
        if 'quantidade' in request.POST:
            produto = get_object_or_404(Produto, id=int(request.POST.get('produto_id')))
            quantidade = int(request.POST.get('quantidade', 1))
            
            for _ in range(quantidade):
                item, _ = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
                item.quantidade += 1
                item.save()


        if 'increment' in request.POST:
            item_removido = True
            item = get_object_or_404(ItemCarrinho, id=int(request.POST.get('carrinho_id')))
            carrinho = item.carrinho
            item_removido = True
            increment = request.POST.get('increment', None)
            if increment == 'true':
                item.quantidade += 1
            elif increment == 'false':
                if item.quantidade > 1:
                    item.quantidade -= 1
            item.save()
            


        # Atualizar os subtotais dos itens
        itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
        
        for item in itens_carrinho:
            item.subtotal = calcular_subtotal(item)
            item.save()

    itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
    teste = ItemCarrinho.objects.filter(carrinho=carrinho).distinct()
    contador_itens = teste.aggregate(total=Sum('quantidade'))['total']
    # Calcule o total do carrinho
    total = sum(item.subtotal for item in itens_carrinho)


    

    context = {
        'categoria_id': 1,
        'produtos': produtos,
        'destaque' : destaque,
        'categorias': categorias,
        'itens_carrinho': itens_carrinho,
        'total': total,
        'contador_itens':contador_itens,
        'item_removido': item_removido,
    }
   
    return render(request,'index.html', context)


def enviar_mensagem_whatsapp(request, tipo):
    # Recupere os itens do carrinho e o total
    carrinho, created = Carrinho.objects.get_or_create()
    itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
    total = sum(item.subtotal for item in itens_carrinho)
   

    # Crie a mensagem com os itens do carrinho e o total
    mensagem = "Itens do carrinho:\n"
    for item in itens_carrinho:
        mensagem += f"{item.quantidade}x {item.produto.nome}\n"

    mensagem += f"\nTotal: {total}"

    if tipo == "mob":
            return HttpResponseRedirect(f"https://api.whatsapp.com/send?phone=5516993307013&text={mensagem}")


    return HttpResponseRedirect(f"https://web.whatsapp.com/send?phone=5516993307013&text={mensagem}")



def produto_list(request, id):
    categorias = Categoria.objects.filter(ativo=True).annotate(num_produtos=Count('produto')).exclude(num_produtos=0)

    if id:
        categoria = get_object_or_404(Categoria, id=id)
        produtos = Produto.objects.filter(categoria=categoria)
    else:
        produtos = Produto.objects.all()

    # Verifique se o carrinho existe ou crie um novo carrinho
    carrinho, created = Carrinho.objects.get_or_create()

    # Obtenha todos os itens do carrinho
    itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)

    # Calcule o total do carrinho
    total = sum(item.subtotal for item in itens_carrinho)

    # Adicione as informações do carrinho ao contexto
    context = {
        'categoria_id': id,
        'produtos': produtos,
        'categorias': categorias,
        'itens_carrinho': itens_carrinho,
        'total': total
    }

    return render(request, 'produto/produto_list.html', context)

def adicionar_item_carrinho(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    carrinho, created = Carrinho.objects.get_or_create()

    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 1))

        # Atualizar os itens do carrinho
        for _ in range(quantidade):
            item, _ = ItemCarrinho.objects.get_or_create(carrinho=carrinho, produto=produto)
            item.quantidade += 1
            item.save()

        # Atualizar os subtotais dos itens
        itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
        for item in itens_carrinho:
            item.subtotal = calcular_subtotal(item)
            item.save()

    # Atualizar as informações do carrinho
    itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
    total = sum(item.subtotal for item in itens_carrinho)
    categorias = Categoria.objects.filter(ativo=True).annotate(num_produtos=Count('produto')).exclude(num_produtos=0)
    produtos = Produto.objects.filter(categoria=produto.categoria)
    
    return render(request, 'produto/produto_list.html', {'produtos': produtos, 'categorias': categorias, 'itens_carrinho': itens_carrinho, 'total': total,'categoria_id': produto.categoria.id,})

def remover_item_carrinho(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id)
    #categoria_id = item.produto.categoria.id
    item.delete()
 
    #return redirect('produto:home')
    return HttpResponseRedirect(reverse('produto:home') + '?item_removido=true')
    

def calcular_subtotal(item):
    return item.produto.valor * item.quantidade


def atualizar_quantidade(request, item_id):
    item = get_object_or_404(ItemCarrinho, id=item_id)
    carrinho = item.carrinho

    if request.method == 'POST':
        increment = request.POST.get('increment', None)
        if increment == 'true':
            item.quantidade += 1
        elif increment == 'false':
            if item.quantidade > 1:
                item.quantidade -= 1
        item.save()
        
        id = request.POST.get('categoria_id',1)
        # Atualizar os subtotais dos itens
        itens_carrinho = ItemCarrinho.objects.filter(carrinho=carrinho)
        for item in itens_carrinho:
            item.subtotal = calcular_subtotal(item)
            item.save()

        total = sum(item.subtotal for item in itens_carrinho)

        categorias = Categoria.objects.filter(ativo=True).annotate(num_produtos=Count('produto')).exclude(num_produtos=0)
        produtos = Produto.objects.filter(categoria=item.produto.categoria)
        
        #return render(request, 'produto/produto_list.html', {'produtos': produtos, 'categorias': categorias, 'itens_carrinho': itens_carrinho, 'total': total})
        return redirect('produto:produto_list', id=id)
    return HttpResponse('Método de requisição inválido.')
