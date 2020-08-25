# Generated by Django 3.1 on 2020-08-25 12:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=15)),
                ('percent', models.FloatField()),
                ('is_active', models.BooleanField(default=True)),
                ('multiple_use', models.BooleanField(default=False)),
            ],
        ),
    ]
