# Generated by Django 5.0.4 on 2024-06-20 19:07

import databaseGen.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Schema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'schema',
            },
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('schema', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='databaseGen.schema')),
            ],
            options={
                'db_table': 'table',
            },
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='VARCHAR', max_length=8)),
                ('name', models.CharField(max_length=30)),
                ('options', models.JSONField(default=databaseGen.models.Field.getDefaultStringOptions)),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='databaseGen.table')),
            ],
            options={
                'db_table': 'field',
            },
        ),
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(default='one to many', max_length=12)),
                ('table1', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='table1', to='databaseGen.table')),
                ('table2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='table2', to='databaseGen.table')),
            ],
            options={
                'db_table': 'association',
            },
        ),
    ]
