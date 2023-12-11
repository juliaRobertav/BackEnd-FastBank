# Generated by Django 4.2.7 on 2023-12-05 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_cadastro_tentativas'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='cartao_credito',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='credito',
            name='cvv',
            field=models.SmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='credito',
            name='limite',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='parcelas',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='valor_parcela',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]