# Generated by Django 5.0.3 on 2024-04-03 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_remove_barbershop_user_barbershop_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='styleofcut',
            name='name',
            field=models.CharField(default='Default Style', max_length=100),
        ),
        migrations.AlterField(
            model_name='styleofcut',
            name='price',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=8),
        ),
    ]
