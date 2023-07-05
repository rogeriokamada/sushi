from django.db import models
from sorl.thumbnail import ImageField
from django.template.defaultfilters import slugify  
from django.urls import reverse

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    ativo = models.BooleanField(choices=[(True, 'Sim'), (False, 'Não')], default=True)
    slug = models.SlugField(null=False)
    order = models.IntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    quantidade = models.IntegerField()
    valor = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    descricao = models.TextField(null=True,)
    destaque = models.BooleanField(default=False)
    promocao = models.BooleanField(default=False)
    ativo = models.BooleanField(default=True)
    imagem = ImageField(upload_to='produtos/%Y/', default="img/padrao.jpg", null=True, blank=True)
    order = models.IntegerField(default=0, blank=False, null=False)

    class Meta:
        ordering = ['order']

    def __str__(self) -> str:
        return self.nome

class Carrinho(models.Model):
    produtos = models.ManyToManyField(Produto, through='ItemCarrinho')

class ItemCarrinho(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    carrinho = models.ForeignKey(Carrinho, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    

