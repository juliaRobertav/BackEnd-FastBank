# Generated by Django 4.2.7 on 2023-12-06 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_remove_emprestimo_conta_alter_emprestimo_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='logado',
            field=models.BooleanField(default=False),
        ),
    ]
