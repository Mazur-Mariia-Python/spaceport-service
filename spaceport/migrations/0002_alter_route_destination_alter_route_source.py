# Generated by Django 5.0.4 on 2024-04-25 13:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spaceport", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="route",
            name="destination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="spaceports_destinations",
                to="spaceport.spaceport",
            ),
        ),
        migrations.AlterField(
            model_name="route",
            name="source",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="spaceports_sources",
                to="spaceport.spaceport",
            ),
        ),
    ]
