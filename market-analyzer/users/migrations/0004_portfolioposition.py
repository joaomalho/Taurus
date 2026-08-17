import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_user_trading_prefs"),
    ]

    operations = [
        migrations.CreateModel(
            name="PortfolioPosition",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("symbol", models.CharField(max_length=10)),
                (
                    "shares",
                    models.DecimalField(
                        decimal_places=4,
                        max_digits=12,
                        validators=[django.core.validators.MinValueValidator(0.0001)],
                    ),
                ),
                (
                    "avg_cost",
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        max_digits=12,
                        null=True,
                        validators=[django.core.validators.MinValueValidator(0.0001)],
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="portfolio_positions",
                        to="users.user",
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="portfolioposition",
            constraint=models.UniqueConstraint(
                fields=("user", "symbol"),
                name="unique_portfolio_symbol_per_user",
            ),
        ),
    ]
