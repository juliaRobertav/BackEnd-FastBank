# Generated by Django 4.2.7 on 2023-12-05 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_login_email_alter_login_senha'),
    ]

    operations = [
        migrations.AddField(
            model_name='cadastro',
            name='tentativas',
            field=models.IntegerField(default=0),
        ),
    ]