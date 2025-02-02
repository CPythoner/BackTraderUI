# Generated by Django 4.1 on 2024-05-24 02:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("backend", "0003_stockpricebjse_ma10_stockpricebjse_ma20_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="stockpricesse",
            name="ma10",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stockpricesse",
            name="ma20",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stockpricesse",
            name="ma30",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stockpricesse",
            name="ma5",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stockpriceszse",
            name="ma10",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stockpriceszse",
            name="ma20",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stockpriceszse",
            name="ma30",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="stockpriceszse",
            name="ma5",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
