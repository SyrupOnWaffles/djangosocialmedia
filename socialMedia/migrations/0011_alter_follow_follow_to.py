# Generated by Django 4.2.12 on 2024-10-03 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('socialMedia', '0010_remove_follow_unique_follow_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='follow_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to='socialMedia.userprofile'),
        ),
    ]
