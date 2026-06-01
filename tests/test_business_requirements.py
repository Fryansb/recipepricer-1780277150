import asyncio
import pytest
from decimal import Decimal
from pydantic import ValidationError

from app.models import IngredientInput, RecipeCalculateRequest, RecipeCalculateResponse, IngredientCost
from app.services.pricing_service import PricingService


class TestRuleOfThreeCalculation:
    """Test the rule of three calculation for ingredient costs."""

    def test_rule_of_three_basic(self):
        """Test: $10 package for 1kg, use 500g = $5.00.
        Formula: (quantidade / peso) * custo = custo_ingrediente
        """
        ingredient = IngredientInput(
            ingredient_name="wheat flour",
            custo_embalagem_fechada="10.00",
            peso_embalagem_fechada="1000",  # 1kg
            quantidade_usada="500"
        )
        service = PricingService()
        cost = service.calculate_ingredient_cost(ingredient)
        assert cost == Decimal("5.00")  # (500/1000) * 10 = 5

    def test_rule_of_three_fractional(self):
        """Test: $5.50 package for 2 liters, use 750ml = $2.06."""
        ingredient = IngredientInput(
            ingredient_name="milk",
            custo_embalagem_fechada="5.50",
            peso_embalagem_fechada="2000",  # 2L
            quantidade_usada="750"
        )
        service = PricingService()
        cost = service.calculate_ingredient_cost(ingredient)
        assert cost == Decimal("2.06")  # (750/2000) * 5.50 = 2.0625 -> 2.06

    def test_rule_of_three_small_amount(self):
        """Test: $2.99 package for 500g, use 10g = $0.06."""
        ingredient = IngredientInput(
            ingredient_name="spice",
            custo_embalagem_fechada="2.99",
            peso_embalagem_fechada="500",
            quantidade_usada="10"
        )
        service = PricingService()
        cost = service.calculate_ingredient_cost(ingredient)
        assert cost == Decimal("0.06")  # (10/500) * 2.99 = 0.0598 -> 0.06


class TestRendimentoCalculation:
    """Test the rendimento (yield) calculation."""

    def test_rendimento_single_unit(self):
        """Test: Total $10, rendimento 1 = $10 unit cost."""
        request = RecipeCalculateRequest(
            ingredients=[
                IngredientInput(
                    ingredient_name="ingredient",
                    custo_embalagem_fechada="10.00",
                    peso_embalagem_fechada="1000",
                    quantidade_usada="1000"
                )
            ],
            rendimento=1,
            margem_lucro=Decimal("0")
        )
        service = PricingService()
        response = asyncio.run(service.calculate_price(request))
        assert response.custo_total == Decimal("10.00")
        assert response.custo_unitario == Decimal("10.00")
        assert response.rendimento == 1

    def test_rendimento_multiple_units(self):
        """Test: Total $100, rendimento 10 = $10 unit cost."""
        request = RecipeCalculateRequest(
            ingredients=[
                IngredientInput(
                    ingredient_name="ingredient",
                    custo_embalagem_fechada="100.00",
                    peso_embalagem_fechada="1000",
                    quantidade_usada="1000"
                )
            ],
            rendimento=10,
            margem_lucro=Decimal("100")
        )
        service = PricingService()
        response = asyncio.run(service.calculate_price(request))
        assert response.custo_unitario == Decimal("10.00")


class TestMargemLucroCalculation:
    """Test the profit margin calculation."""

    def test_margem_zero(self):
        """Test: 0% margin = same price as cost."""
        request = RecipeCalculateRequest(
            ingredients=[
                IngredientInput(
                    ingredient_name="test",
                    custo_embalagem_fechada="10.00",
                    peso_embalagem_fechada="1000",
                    quantidade_usada="1000"
                )
            ],
            rendimento=1,
            margem_lucro=Decimal("0")
        )
        service = PricingService()
        response = asyncio.run(service.calculate_price(request))
        assert response.preco_final_sugerido == Decimal("10.00")

    def test_margem_100_percent(self):
        """Test: 100% margin = double the cost."""
        request = RecipeCalculateRequest(
            ingredients=[
                IngredientInput(
                    ingredient_name="test",
                    custo_embalagem_fechada="10.00",
                    peso_embalagem_fechada="1000",
                    quantidade_usada="1000"
                )
            ],
            rendimento=1,
            margem_lucro=Decimal("100")
        )
        service = PricingService()
        response = asyncio.run(service.calculate_price(request))
        assert response.preco_final_sugerido == Decimal("20.00")

    def test_margem_150_percent(self):
        """Test: 150% margin = 2.5x the cost."""
        request = RecipeCalculateRequest(
            ingredients=[
                IngredientInput(
                    ingredient_name="test",
                    custo_embalagem_fechada="8.00",
                    peso_embalagem_fechada="1000",
                    quantidade_usada="1000"
                )
            ],
            rendimento=1,
            margem_lucro=Decimal("150")
        )
        service = PricingService()
        response = asyncio.run(service.calculate_price(request))
        assert response.preco_final_sugerido == Decimal("20.00")

    def test_margem_with_multiple_ingredients(self):
        """Test margin with total cost calculation."""
        request = RecipeCalculateRequest(
            ingredients=[
                IngredientInput(ingredient_name="flour", custo_embalagem_fechada="5.00", peso_embalagem_fechada="1000", quantidade_usada="500"),
                IngredientInput(ingredient_name="eggs", custo_embalagem_fechada="6.00", peso_embalagem_fechada="12", quantidade_usada="2"),
            ],
            rendimento=10,
            margem_lucro=Decimal("50")
        )
        service = PricingService()
        response = asyncio.run(service.calculate_price(request))
        assert response.custo_total == Decimal("3.50")
        assert response.custo_unitario == Decimal("0.35")
        assert response.preco_final_sugerido == Decimal("0.53")


class TestAllReturnValues:
    """Test that ALL required return values are present."""

    def test_response_has_all_fields(self):
        """Verify RecipeCalculateResponse has all 6 required fields."""
        request = RecipeCalculateRequest(
            ingredients=[
                IngredientInput(
                    ingredient_name="flour",
                    custo_embalagem_fechada="10.00",
                    peso_embalagem_fechada="1000",
                    quantidade_usada="500"
                )
            ],
            rendimento=12,
            margem_lucro=Decimal("100")
        )
        service = PricingService()
        response = asyncio.run(service.calculate_price(request))
        
        assert hasattr(response, 'custo_total')
        assert hasattr(response, 'custo_unitario')
        assert hasattr(response, 'preco_final_sugerido')
        assert hasattr(response, 'rendimento')
        assert hasattr(response, 'margem_lucro')
        assert hasattr(response, 'ingredient_costs')

    def test_response_ingredient_costs_has_breakdown(self):
        """Each ingredient cost must include all breakdown fields."""
        request = RecipeCalculateRequest(
            ingredients=[
                IngredientInput(
                    ingredient_name="flour",
                    custo_embalagem_fechada="10.00",
                    peso_embalagem_fechada="1000",
                    quantidade_usada="500"
                )
            ],
            rendimento=10,
            margem_lucro=Decimal("150")
        )
        service = PricingService()
        response = asyncio.run(service.calculate_price(request))
        
        assert len(response.ingredient_costs) == 1
        ing_cost = response.ingredient_costs[0]
        assert ing_cost.ingredient_name == "flour"
        assert ing_cost.custo_ingrediente is not None