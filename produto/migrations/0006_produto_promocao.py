# Generated by Django 4.2.2 on 2023-06-19 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0005_alter_produto_descricao_alter_produto_imagem'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='promocao',
            field=models.BooleanField(default=False),
        ),
    ]
