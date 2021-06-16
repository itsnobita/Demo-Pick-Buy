# Generated by Django 3.1.3 on 2021-04-17 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order_placed',
            old_name='ordered_state',
            new_name='status',
        ),
        migrations.AddField(
            model_name='order_placed',
            name='ordered_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
