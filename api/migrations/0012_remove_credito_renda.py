# Generated by Django 4.2.7 on 2023-12-05 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_cliente_cartao_credito_credito_cvv_credito_limite_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credito',
            name='renda',
        ),
    ]
