# Generated by Django 4.2.7 on 2023-12-04 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_rename_conta_transacao_conta_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='login',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='login',
            name='senha',
            field=models.CharField(max_length=50),
        ),
    ]
