# Generated by Django 4.1.5 on 2023-03-01 21:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_tags'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('-modify_dt',)},
        ),
    ]
