"""Pydantic models for RecipePricer API."""

from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from pydantic import BaseModel, Field, field_validator


class IngredientInput(BaseModel):
    """
    Ingredient input model for recipe pricing calculations.
    
    Attributes:
        ingredient_name: Name of the ingredient (1-100 characters)
        custo_embalagem_fechada: Cost of the closed package (positive, 2 decimal places)
        peso_embalagem_fechada: Weight/volume of the closed package (positive, 4 decimal places)
        quantidade_usada: Amount used in recipe (non-negative, 4 decimal places)
    """
    
    ingredient_name: str = Field(..., min_length=1, max_length=100, description="Ingredient name (1-100 chars)")
    custo_embalagem_fechada: Decimal = Field(..., gt=0, description="Cost of closed package (positive, 2 decimal places)")
    peso_embalagem_fechada: Decimal = Field(..., gt=0, description="Weight/volume of closed package (positive, 4 decimal places)")
    quantidade_usada: Decimal = Field(..., ge=0, description="Amount used in recipe (non-negative, 4 decimal places)")
    
    @field_validator("custo_embalagem_fechada", mode="before")
    @classmethod
    def quantize_custo_embalagem_fechada(cls, v: Any) -> Decimal:
        """Convert to Decimal and quantize custo_embalagem_fechada to 2 decimal places using ROUND_HALF_UP."""
        if isinstance(v, (int, float)):
            v = Decimal(str(v))
        return Decimal(v).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    
    @field_validator("peso_embalagem_fechada", mode="before")
    @classmethod
    def quantize_peso_embalagem_fechada(cls, v: Any) -> Decimal:
        """Convert to Decimal and quantize peso_embalagem_fechada to 4 decimal places using ROUND_HALF_UP."""
        if isinstance(v, (int, float)):
            v = Decimal(str(v))
        return Decimal(v).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    
    @field_validator("quantidade_usada", mode="before")
    @classmethod
    def quantize_quantidade_usada(cls, v: Any) -> Decimal:
        """Convert to Decimal and quantize quantidade_usada to 4 decimal places using ROUND_HALF_UP."""
        if isinstance(v, (int, float)):
            v = Decimal(str(v))
        return Decimal(v).quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)


class IngredientCost(BaseModel):
    """Response model for individual ingredient cost breakdown.
    
    Attributes:
        ingredient_name: Name of the ingredient
        quantidade_usada: Amount used
        custo_embalagem_fechada: Package cost
        peso_embalagem_fechada: Package weight/volume
        custo_ingrediente: Calculated cost for this ingredient (rule of three)
    """
    ingredient_name: str = Field(..., description="Ingredient name")
    quantidade_usada: Decimal = Field(..., description="Amount used")
    custo_embalagem_fechada: Decimal = Field(..., description="Package cost")
    peso_embalagem_fechada: Decimal = Field(..., description="Package weight/volume")
    custo_ingrediente: Decimal = Field(..., description="Calculated ingredient cost")

    @field_validator("quantidade_usada", "custo_embalagem_fechada", "peso_embalagem_fechada", "custo_ingrediente", mode="before")
    @classmethod
    def parse_decimals(cls, v: Any) -> Decimal:
        """Parse all decimal fields."""
        if isinstance(v, (int, float)):
            v = Decimal(str(v))
        return Decimal(v).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class RecipeCalculateRequest(BaseModel):
    """Request model for calculating recipe costs.
    
    Attributes:
        ingredients: List of ingredients with package info
        rendimento: Number of units the recipe produces (REQUIRED business field)
        margem_lucro: Profit margin percentage (ex: 150 = 150% profit) (REQUIRED business field)
    """
    ingredients: list[IngredientInput] = Field(..., min_length=1, description="List of ingredients")
    rendimento: int = Field(..., gt=0, description="Recipe yield - units produced (REQUIRED)")
    margem_lucro: Decimal = Field(..., ge=0, description="Profit margin percentage, ex: 150 = 150% (REQUIRED)")

    @field_validator("margem_lucro", mode="before")
    @classmethod
    def parse_margem_lucro(cls, v: Any) -> Decimal:
        """Parse margin to Decimal."""
        if isinstance(v, (int, float)):
            v = Decimal(str(v))
        return Decimal(v).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


class RecipeCalculateResponse(BaseModel):
    """Response model for recipe cost calculation.
    
    Attributes:
        custo_total: Total cost of all ingredients combined (rule of three calculation)
        custo_unitario: Cost per unit (custo_total / rendimento)
        preco_final_sugerido: Suggested selling price (custo_unitario * (1 + margem/100))
        rendimento: Units produced (echo back)
        margem_lucro: Profit margin used (echo back)
        ingredient_costs: Individual ingredient cost breakdown
    """
    custo_total: Decimal = Field(..., description="Total cost of all ingredients")
    custo_unitario: Decimal = Field(..., description="Cost per unit produced")
    preco_final_sugerido: Decimal = Field(..., description="Suggested selling price with margin")
    rendimento: int = Field(..., description="Recipe yield - units produced")
    margem_lucro: Decimal = Field(..., description="Profit margin used")
    ingredient_costs: list[IngredientCost] = Field(default_factory=list, description="Ingredient breakdown")

    @field_validator("custo_total", "custo_unitario", "preco_final_sugerido", "margem_lucro", mode="before")
    @classmethod
    def parse_decimals(cls, v: Any) -> Decimal:
        """Parse all decimal fields to 2 decimal places."""
        if isinstance(v, (int, float)):
            v = Decimal(str(v))
        return Decimal(v).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)