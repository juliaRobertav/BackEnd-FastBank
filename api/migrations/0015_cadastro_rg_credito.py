

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_emprestimo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cadastro',
            name='rg',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.CreateModel(
            name='Credito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('renda', models.FloatField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.contas')),
            ],
        ),
    ]
