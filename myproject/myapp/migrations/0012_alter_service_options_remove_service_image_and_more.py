# Generated by Django 5.1.2 on 2024-11-08 13:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_service_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={},
        ),
        migrations.RemoveField(
            model_name='service',
            name='image',
        ),
        migrations.CreateModel(
            name='ServiceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='service_images/', verbose_name='Фото')),
                ('order', models.PositiveIntegerField(default=0, verbose_name='Порядок отображения')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='myapp.service')),
            ],
            options={
                'verbose_name': 'Фото услуги',
                'verbose_name_plural': 'Фото услуг',
                'ordering': ['order'],
            },
        ),
    ]
