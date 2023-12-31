# Generated by Django 4.2.7 on 2023-12-06 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_login_logado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transacao',
            old_name='conta_cliente',
            new_name='conta_enviando',
        ),
        migrations.RemoveField(
            model_name='cliente',
            name='cartao_credito',
        ),
        migrations.AddField(
            model_name='transacao',
            name='conta_recebendo',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='descricao',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='valor',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
