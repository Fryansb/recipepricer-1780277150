"""Tests for IngredientInput model."""

import pytest
from decimal import Decimal

from app.models import IngredientInput


class TestIngredientInput:
    """Test suite for IngredientInput model validations."""

    def test_valid_ingredient_input(self):
        """Test creating a valid ingredient with all fields."""
        ingredient = IngredientInput(
            ingredient_name="Flour",
            custo_embalagem_fechada=Decimal("5.00"),
            peso_embalagem_fechada=Decimal("1000.0000"),
            quantidade_usada=Decimal("250.0000")
        )
        
        assert ingredient.ingredient_name == "Flour"
        assert ingredient.custo_embalagem_fechada == Decimal("5.00")
        assert ingredient.peso_embalagem_fechada == Decimal("1000.0000")
        assert ingredient.quantidade_usada == Decimal("250.0000")

    def test_ingredient_name_min_length(self):
        """Test ingredient_name with minimum length (1 char)."""
        ingredient = IngredientInput(
            ingredient_name="A",
            custo_embalagem_fechada=Decimal("5.00"),
            peso_embalagem_fechada=Decimal("1000.0000"),
            quantidade_usada=Decimal("250.0000")
        )
        assert ingredient.ingredient_name == "A"

    def test_ingredient_name_max_length(self):
        """Test ingredient_name with maximum length (100 chars)."""
        name_100 = "A" * 100
        ingredient = IngredientInput(
            ingredient_name=name_100,
            custo_embalagem_fechada=Decimal("5.00"),
            peso_embalagem_fechada=Decimal("1000.0000"),
            quantidade_usada=Decimal("250.0000")
        )
        assert ingredient.ingredient_name == name_100

    def test_ingredient_name_too_long(self):
        """Test ingredient_name with more than 100 chars raises error."""
        name_101 = "A" * 101
        with pytest.raises(ValueError):
            IngredientInput(
                ingredient_name=name_101,
                custo_embalagem_fechada=Decimal("5.00"),
                peso_embalagem_fechada=Decimal("1000.0000"),
                quantidade_usada=Decimal("250.0000")
            )

    def test_ingredient_name_empty(self):
        """Test empty ingredient_name raises error."""
        with pytest.raises(ValueError):
            IngredientInput(
                ingredient_name="",
                custo_embalagem_fechada=Decimal("5.00"),
                peso_embalagem_fechada=Decimal("1000.0000"),
                quantidade_usada=Decimal("250.0000")
            )

    def test_custo_embalagem_fechada_positive(self):
        """Test custo_embalagem_fechada is positive."""
        ingredient = IngredientInput(
            ingredient_name="Flour",
            custo_embalagem_fechada=Decimal("0.01"),
            peso_embalagem_fechada=Decimal("1000.0000"),
            quantidade_usada=Decimal("250.0000")
        )
        assert ingredient.custo_embalagem_fechada == Decimal("0.01")

    def test_custo_embalagem_fechada_zero_raises_error(self):
        """Test custo_embalagem_fechada of zero raises error."""
        with pytest.raises(ValueError):
            IngredientInput(
                ingredient_name="Flour",
                custo_embalagem_fechada=Decimal("0"),
                peso_embalagem_fechada=Decimal("1000.0000"),
                quantidade_usada=Decimal("250.0000")
            )

    def test_custo_embalagem_fechada_negative_raises_error(self):
        """Test custo_embalagem_fechada negative raises error."""
        with pytest.raises(ValueError):
            IngredientInput(
                ingredient_name="Flour",
                custo_embalagem_fechada=Decimal("-5.00"),
                peso_embalagem_fechada=Decimal("1000.0000"),
                quantidade_usada=Decimal("250.0000")
            )

    def test_custo_embalagem_fechada_2_decimal_places(self):
        """Test custo_embalagem_fechada quantizes to 2 decimal places."""
        ingredient = IngredientInput(
            ingredient_name="Flour",
            custo_embalagem_fechada=Decimal("5.555"),
            peso_embalagem_fechada=Decimal("1000.0000"),
            quantidade_usada=Decimal("250.0000")
        )
        assert ingredient.custo_embalagem_fechada == Decimal("5.56")  # Rounded with ROUND_HALF_UP

    def test_peso_embalagem_fechada_positive(self):
        """Test peso_embalagem_fechada is positive."""
        ingredient = IngredientInput(
            ingredient_name="Flour",
            custo_embalagem_fechada=Decimal("5.00"),
            peso_embalagem_fechada=Decimal("0.0001"),
            quantidade_usada=Decimal("250.0000")
        )
        assert ingredient.peso_embalagem_fechada == Decimal("0.0001")

    def test_peso_embalagem_fechada_zero_raises_error(self):
        """Test peso_embalagem_fechada of zero raises error."""
        with pytest.raises(ValueError):
            IngredientInput(
                ingredient_name="Flour",
                custo_embalagem_fechada=Decimal("5.00"),
                peso_embalagem_fechada=Decimal("0"),
                quantidade_usada=Decimal("250.0000")
            )

    def test_peso_embalagem_fechada_negative_raises_error(self):
        """Test peso_embalagem_fechada negative raises error."""
        with pytest.raises(ValueError):
            IngredientInput(
                ingredient_name="Flour",
                custo_embalagem_fechada=Decimal("5.00"),
                peso_embalagem_fechada=Decimal("-1000.0000"),
                quantidade_usada=Decimal("250.0000")
            )

    def test_peso_embalagem_fechada_4_decimal_places(self):
        """Test peso_embalagem_fechada quantizes to 4 decimal places."""
        ingredient = IngredientInput(
            ingredient_name="Flour",
            custo_embalagem_fechada=Decimal("5.00"),
            peso_embalagem_fechada=Decimal("999.9998"),  # Will quantize to 4 places
            quantidade_usada=Decimal("250.0000")
        )
        assert ingredient.peso_embalagem_fechada == Decimal("999.9998")  # Exact 4 places

    def test_quantidade_usada_zero_allowed(self):
        """Test quantidade_usada can be zero (non-negative)."""
        ingredient = IngredientInput(
            ingredient_name="Flour",
            custo_embalagem_fechada=Decimal("5.00"),
            peso_embalagem_fechada=Decimal("1000.0000"),
            quantidade_usada=Decimal("0")
        )
        assert ingredient.quantidade_usada == Decimal("0.0000")

    def test_quantidade_usada_positive(self):
        """Test quantidade_usada with positive value."""
        ingredient = IngredientInput(
            ingredient_name="Flour",
            custo_embalagem_fechada=Decimal("5.00"),
            peso_embalagem_fechada=Decimal("1000.0000"),
            quantidade_usada=Decimal("250.5000")
        )
        assert ingredient.quantidade_usada == Decimal("250.5000")

    def test_quantidade_usada_negative_raises_error(self):
        """Test quantidade_usada negative raises error."""
        with pytest.raises(ValueError):
            IngredientInput(
                ingredient_name="Flour",
                custo_embalagem_fechada=Decimal("5.00"),
                peso_embalagem_fechada=Decimal("1000.0000"),
                quantidade_usada=Decimal("-250.0000")
            )

    def test_quantidade_usada_4_decimal_places(self):
        """Test quantidade_usada quantizes to 4 decimal places."""
        ingredient = IngredientInput(
            ingredient_name="Flour",
            custo_embalagem_fechada=Decimal("5.00"),
            peso_embalagem_fechada=Decimal("1000.0000"),
            quantidade_usada=Decimal("250.00005")
        )
        assert ingredient.quantidade_usada == Decimal("250.0001")  # Rounded with ROUND_HALF_UP

    def test_string_input_coercion_to_decimal(self):
        """Test that string inputs are coerced to Decimal."""
        ingredient = IngredientInput(
            ingredient_name="Flour",
            custo_embalagem_fechada="5.00",  # String input
            peso_embalagem_fechada="1000.0000",  # String input
            quantidade_usada="250.50"  # String input
        )
        assert ingredient.custo_embalagem_fechada == Decimal("5.00")
        assert ingredient.peso_embalagem_fechada == Decimal("1000.0000")
        assert ingredient.quantidade_usada == Decimal("250.5000")
    
    def test_float_input_coercion_to_decimal(self):
        """Test that float inputs are coerced to Decimal."""
        ingredient = IngredientInput(
            ingredient_name="Flour",
            custo_embalagem_fechada=5.555,  # Float input
            peso_embalagem_fechada=1000.12345,  # Float input
            quantidade_usada=250.5  # Float input
        )
        assert ingredient.custo_embalagem_fechada == Decimal("5.56")
        assert ingredient.peso_embalagem_fechada == Decimal("1000.1235")
        assert ingredient.quantidade_usada == Decimal("250.5000")

    def test_int_input_coercion_to_decimal(self):
        """Test that int inputs are coerced to Decimal."""
        ingredient = IngredientInput(
            ingredient_name="Flour",
            custo_embalagem_fechada=5,  # Int input
            peso_embalagem_fechada=1000,  # Int input
            quantidade_usada=250  # Int input
        )
        assert ingredient.custo_embalagem_fechada == Decimal("5.00")
        assert ingredient.peso_embalagem_fechada == Decimal("1000.0000")
        assert ingredient.quantidade_usada == Decimal("250.0000")