# Generated by Django 3.0.3 on 2020-03-31 14:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0009_post_view_count'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-id',)},
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=115),
        ),
    ]
