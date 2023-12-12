# Generated by Django 4.2.7 on 2023-12-12 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_rename_conta_cliente_transacao_conta_enviando_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Saldo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saldo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='saldo_cliente', to='api.cliente')),
            ],
        ),
    ]