# Generated by Django 5.0.4 on 2024-04-25 14:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("spaceport", "0002_alter_route_destination_alter_route_source"),
    ]

    operations = [
        migrations.AlterField(
            model_name="route",
            name="destination",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="destinations",
                to="spaceport.spaceport",
            ),
        ),
        migrations.AlterField(
            model_name="route",
            name="source",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sources",
                to="spaceport.spaceport",
            ),
        ),
    ]
