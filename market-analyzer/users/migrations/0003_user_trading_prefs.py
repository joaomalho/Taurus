from decimal import Decimal

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_watchlistitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="portfolio_value",
            field=models.DecimalField(
                decimal_places=2,
                default=10000,
                max_digits=12,
                validators=[
                    django.core.validators.MinValueValidator(100),
                    django.core.validators.MaxValueValidator(10000000),
                ],
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="risk_percent",
            field=models.DecimalField(
                decimal_places=2,
                default=2.0,
                max_digits=5,
                validators=[
                    django.core.validators.MinValueValidator(0.1),
                    django.core.validators.MaxValueValidator(10),
                ],
            ),
        ),
    ]
