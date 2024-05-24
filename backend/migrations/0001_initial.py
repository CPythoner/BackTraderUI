# Generated by Django 4.1 on 2024-05-23 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "a_stock_code",
                    models.CharField(default="TEMP_CODE", max_length=10, unique=True),
                ),
                (
                    "b_stock_code",
                    models.CharField(blank=True, max_length=10, null=True),
                ),
                ("abbreviation", models.CharField(default="TEMP_ABBR", max_length=100)),
                (
                    "full_abbreviation",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                (
                    "english_name",
                    models.CharField(blank=True, max_length=200, null=True),
                ),
                ("list_date", models.DateField(blank=True, null=True)),
                (
                    "market",
                    models.CharField(
                        choices=[("SSE", "上证"), ("SZSE", "深证"), ("BJSE", "北交所")],
                        default="SSE",
                        max_length=4,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StockPriceSZSE",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("open", models.FloatField()),
                ("high", models.FloatField()),
                ("low", models.FloatField()),
                ("close", models.FloatField()),
                ("volume", models.BigIntegerField()),
                ("turnover", models.FloatField()),
                (
                    "stock",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prices_szse",
                        to="backend.stock",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StockPriceSSE",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("open", models.FloatField()),
                ("high", models.FloatField()),
                ("low", models.FloatField()),
                ("close", models.FloatField()),
                ("volume", models.BigIntegerField()),
                ("turnover", models.FloatField()),
                (
                    "stock",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prices_sse",
                        to="backend.stock",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StockPriceBJSE",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.DateField()),
                ("open", models.FloatField()),
                ("high", models.FloatField()),
                ("low", models.FloatField()),
                ("close", models.FloatField()),
                ("volume", models.BigIntegerField()),
                ("turnover", models.FloatField()),
                (
                    "stock",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="prices_bjse",
                        to="backend.stock",
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="stockpriceszse",
            index=models.Index(
                fields=["stock", "date"], name="backend_sto_stock_i_a38c16_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="stockpriceszse",
            index=models.Index(fields=["date"], name="backend_sto_date_9c253c_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="stockpriceszse",
            unique_together={("stock", "date")},
        ),
        migrations.AddIndex(
            model_name="stockpricesse",
            index=models.Index(
                fields=["stock", "date"], name="backend_sto_stock_i_fc706c_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="stockpricesse",
            index=models.Index(fields=["date"], name="backend_sto_date_0a5906_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="stockpricesse",
            unique_together={("stock", "date")},
        ),
        migrations.AddIndex(
            model_name="stockpricebjse",
            index=models.Index(
                fields=["stock", "date"], name="backend_sto_stock_i_432c8c_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="stockpricebjse",
            index=models.Index(fields=["date"], name="backend_sto_date_397dd4_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="stockpricebjse",
            unique_together={("stock", "date")},
        ),
    ]
