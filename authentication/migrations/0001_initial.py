# Generated by Django 3.0.6 on 2021-11-19 22:12

from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('_id', djongo.models.fields.ObjectIdField(auto_created=True, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('nombre', models.TextField()),
                ('aPaterno', models.TextField()),
                ('aMaterno', models.TextField()),
                ('rfc', models.TextField(max_length=13, unique=True)),
                ('email', models.TextField(verbose_name='email')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
