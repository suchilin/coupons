# Generated by Django 2.0.5 on 2018-05-16 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField()),
                ('checked_out', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='cart',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='articles', to='articles.Cart'),
        ),
    ]
