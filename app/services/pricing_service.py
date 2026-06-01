"""Pricing service for RecipePricer API with rule of three calculations."""

from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from app.models import IngredientCost, IngredientInput, RecipeCalculateRequest, RecipeCalculateResponse


class PricingService:
    """Service for calculating recipe pricing based on ingredients."""

    def calculate_ingredient_cost(
        self, ingredient: IngredientInput
    ) -> Decimal:
        """Calculate ingredient cost using rule of three.
        
        Formula: (quantidade_usada / peso_embalagem) * custo_embalagem
        Example: If package costs $10 for 1kg, and we use 500g:
                 (500 / 1000) * 10 = $5.00
        """
        # Rule of three: (amount used / package weight) * package cost
        cost = (ingredient.quantidade_usada / ingredient.peso_embalagem_fechada) * ingredient.custo_embalagem_fechada
        return cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def calculate_total_cost(self, ingredients: list[IngredientInput]) -> Decimal:
        """Calculate total cost of all ingredients."""
        total = sum(self.calculate_ingredient_cost(ing) for ing in ingredients)
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def calculate_unit_cost(self, total_cost: Decimal, rendimento: int) -> Decimal:
        """Calculate cost per unit (total / yield)."""
        unit_cost = total_cost / Decimal(str(rendimento))
        return unit_cost.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def calculate_suggested_price(
        self, unit_cost: Decimal, margem_lucro: Decimal
    ) -> Decimal:
        """Calculate suggested selling price with margin.
        
        Formula: unit_cost * (1 + margin/100)
        Example: unit_cost $5.00, margin 150%:
                 5.00 * (1 + 150/100) = $12.50
        """
        # margin is percentage: 150 means 150%
        multiplier = Decimal("1") + (margem_lucro / Decimal("100"))
        final_price = unit_cost * multiplier
        return final_price.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    async def calculate_price(
        self, request: RecipeCalculateRequest
    ) -> RecipeCalculateResponse:
        """Main calculation method - returns full response with all required fields."""
        # Calculate individual ingredient costs
        ingredient_costs = []
        for ing in request.ingredients:
            cost = self.calculate_ingredient_cost(ing)
            ingredient_costs.append(
                IngredientCost(
                    ingredient_name=ing.ingredient_name,
                    quantidade_usada=ing.quantidade_usada,
                    custo_embalagem_fechada=ing.custo_embalagem_fechada,
                    peso_embalagem_fechada=ing.peso_embalagem_fechada,
                    custo_ingrediente=cost,
                )
            )

        # Calculate totals
        custo_total = self.calculate_total_cost(request.ingredients)
        custo_unitario = self.calculate_unit_cost(custo_total, request.rendimento)
        preco_final = self.calculate_suggested_price(custo_unitario, request.margem_lucro)  # Use unit_cost, not total

        return RecipeCalculateResponse(
            custo_total=custo_total,
            custo_unitario=custo_unitario,
            preco_final_sugerido=preco_final,
            rendimento=request.rendimento,
            margem_lucro=request.margem_lucro,
            ingredient_costs=ingredient_costs,
        )