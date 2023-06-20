from django.contrib import admin
from adminsortable2.admin import SortableAdminMixin
from .models import Categoria, Produto

# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(SortableAdminMixin, admin.ModelAdmin):
    pass

@admin.register(Produto)
class ProdutoAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('nome', 'valor', 'categoria','destaque','ativo','promocao')
    list_filter = ('destaque', 'categoria','ativo','promocao')
    list_editable = ('valor','destaque','ativo','promocao')
    search_fields = ('nome',)
    
