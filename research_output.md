# FastAPI Decimal Patterns and Business Requirement Implementation Research

## Table of Contents
1. [Introduction](#introduction)
2. [Decimal Type in Python](#decimal-type-in-python)
3. [Pydantic Decimal Integration](#pydantic-decimal-integration)
4. [FastAPI Decimal Request/Response Patterns](#fastapi-decimal-requestresponse-patterns)
5. [Rule of Three Calculation Patterns](#rule-of-three-calculation-patterns)
6. [Business Logic Implementation Patterns](#business-logic-implementation-patterns)
7. [API Endpoint Design for RecipePricer](#api-endpoint-design-for-recipepricer)
8. [Error Handling and Validation](#error-handling-and-validation)
9. [Testing Strategies](#testing-strategies)
10. [Best Practices Summary](#best-practices-summary)
11. [Complete Implementation Example](#complete-implementation-example)

---

## Introduction

This research document explores implementation patterns for building a FastAPI-based RecipePricer application that performs decimal arithmetic for pricing calculations. The application requires precise financial calculations using Python's `Decimal` type, Pydantic validation, and proper handling of the "rule of three" (regra de três) proportional calculation pattern.

### Key Objectives
- Understand Decimal type handling in FastAPI/Pydantic
- Implement rule of three calculations with proper precision
- Design robust API endpoints for pricing calculations
- Handle business requirements with appropriate validation

---

## Decimal Type in Python

### Overview

Python's `decimal` module provides the `Decimal` type for exact decimal arithmetic, crucial for financial calculations where floating-point precision errors are unacceptable.

### Why Decimal Instead of Float?

Floats use binary floating-point representation, leading to precision errors:

```python
# Float precision issues
>>> 0.1 + 0.2
0.30000000000000004

# Decimal precision
>>> from decimal import Decimal
>>> Decimal('0.1') + Decimal('0.2')
Decimal('0.3')
```

### Decimal Context and Rounding

```python
from decimal import Decimal, getcontext, ROUND_HALF_UP

getcontext().prec = 28
getcontext().rounding = ROUND_HALF_UP
```

Common rounding modes:
- `ROUND_HALF_UP`: Round to nearest, ties away from zero
- `ROUND_HALF_EVEN`: Round to nearest, ties to even (default)
- `ROUND_DOWN`: Round towards zero
- `ROUND_UP`: Round away from zero

### Decimal Arithmetic Operations

```python
from decimal import Decimal, ROUND_HALF_UP

a = Decimal('10.50')
b = Decimal('3.25')

sum_result = a + b
diff_result = a - b
prod_result = a * b
quot_result = a / b

# Quantize for currency precision
price = Decimal('19.999')
quantized = price.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # Decimal('20.00')
```

---

## Pydantic Decimal Integration

### Pydantic v2 Decimal Handling

Pydantic v2 has native support for Decimal types with proper JSON serialization:

```python
from pydantic import BaseModel
from decimal import Decimal

class Ingredient(BaseModel):
    nome: str
    custo_embalagem_fechada: Decimal
    peso_embalagem_fechada: Decimal
    quantidade_usada: Decimal

# Pydantic validates and coerces Decimal inputs
ingredient = Ingredient(
    nome="Flour",
    custo_embalagem_fechada="5.00",
    peso_embalagem_fechada=Decimal("1000"),
    quantidade_usada=250.0
)
```

### Custom Decimal Validation

```python
from pydantic import BaseModel, field_validator
from decimal import Decimal
from typing import Any

class Ingredient(BaseModel):
    nome: str
    custo_embalagem_fechada: Decimal
    peso_embalagem_fechada: Decimal
    quantidade_usada: Decimal

    @field_validator('custo_embalagem_fechada', 'peso_embalagem_fechada', 'quantidade_usada', mode='before')
    @classmethod
    def ensure_decimal(cls, v: Any) -> Decimal:
        if isinstance(v, float):
            return Decimal(str(v))
        return Decimal(v) if not isinstance(v, Decimal) else v
```

### Using Annotated for Decimal Constraints

```python
from pydantic import BaseModel, condecimal
from decimal import Decimal
from typing import Annotated

class Ingredient(BaseModel):
    nome: str
    custo_embalagem_fechada: Annotated[Decimal, condecimal(gt=0, max_digits=10, decimal_places=2)]
    peso_embalagem_fechada: Annotated[Decimal, condecimal(gt=0, max_digits=10, decimal_places=3)]
    quantidade_usada: Annotated[Decimal, condecimal(gt=0, max_digits=10, decimal_places=3)]
```

---

## FastAPI Decimal Request/Response Patterns

### Request Model with Decimal Fields

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import List, Any

app = FastAPI()

class Ingredient(BaseModel):
    nome: str = Field(..., min_length=1, description="Ingredient name")
    custo_embalagem_fechada: Decimal = Field(..., gt=0, description="Package cost")
    peso_embalagem_fechada: Decimal = Field(..., gt=0, description="Package weight/volume")
    quantidade_usada: Decimal = Field(..., gt=0, description="Amount used in recipe")

    @field_validator('custo_embalagem_fechada', 'peso_embalagem_fechada', 'quantidade_usada', mode='before')
    @classmethod
    def convert_to_decimal(cls, v: Any) -> Decimal:
        if isinstance(v, float):
            return Decimal(str(v))
        return Decimal(v) if not isinstance(v, Decimal) else v

class PriceCalculationRequest(BaseModel):
    ingredientes: List[Ingredient] = Field(..., min_length=1)
    rendimento: int = Field(..., gt=0, description="Recipe yield (number of units)")
    margem_lucro: Decimal = Field(..., ge=0, description="Profit margin percentage")

class PriceCalculationResponse(BaseModel):
    custo_total: Decimal = Field(..., description="Total recipe cost")
    custo_unitario: Decimal = Field(..., description="Cost per unit")
    preco_final_sugerido: Decimal = Field(..., description="Suggested final price per unit")

    class Config:
        json_encoders = {Decimal: float}
```

### Using Response Model in FastAPI

```python
@app.post("/calculate-price", response_model=PriceCalculationResponse)
async def calculate_price(request: PriceCalculationRequest):
    return PriceCalculationResponse(
        custo_total=Decimal("8.50"),
        custo_unitario=Decimal("0.85"),
        preco_final_sugerido=Decimal("2.13")
    )
```

---

## Rule of Three Calculation Patterns

### Mathematical Foundation

The "regra de três" (rule of three) is a proportional calculation method.

**Formula**: `(quantidade_usada / peso_embalagem_fechada) × custo_embalagem_fechada = custo_ingrediente`

If 1000g costs R$5.00, then 250g costs: (250 / 1000) × 5.00 = R$1.25

### Implementation Patterns

#### Pattern 1: Basic Rule of Three Function

```python
from decimal import Decimal, ROUND_HALF_UP

def calculate_ingredient_cost(
    quantity_used: Decimal,
    package_weight: Decimal,
    package_cost: Decimal
) -> Decimal:
    if package_weight == 0:
        raise ValueError("Package weight cannot be zero")
    
    cost = (quantity_used / package_weight) * package_cost
    return cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# Example usage
cost = calculate_ingredient_cost(
    quantity_used=Decimal('250'),
    package_weight=Decimal('1000'),
    package_cost=Decimal('5.00')
)
# Result: Decimal('1.25')
```

#### Pattern 2: Class-Based Calculator

```python
from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass
from typing import List

@dataclass
class IngredientData:
    nome: str
    quantidade_usada: Decimal
    peso_embalagem_fechada: Decimal
    custo_embalagem_fechada: Decimal
    
    @property
    def custo_proporcional(self) -> Decimal:
        return ((self.quantidade_usada / self.peso_embalagem_fechada) * self.custo_embalagem_fechada).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def calculate_total_cost(ingredients: List[IngredientData]) -> Decimal:
    total = sum(ing.custo_proporcional for ing in ingredients)
    return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
```

---

## Business Logic Implementation Patterns

### Core Business Logic Flow

1. Validate input data (Pydantic models)
2. Calculate per-ingredient proportional costs
3. Sum all costs to get total
4. Calculate unit cost (total / yield)
5. Apply profit margin to get final price
6. Return formatted response

### Service Layer Approach

```python
from decimal import Decimal, ROUND_HALF_UP
from typing import List

class PricingService:
    @staticmethod
    def calculate_ingredient_cost(ingredient: Ingredient) -> Decimal:
        cost = (ingredient.quantidade_usada / ingredient.peso_embalagem_fechada) * ingredient.custo_embalagem_fechada
        return cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_total_cost(ingredients: List[Ingredient]) -> Decimal:
        total = sum(PricingService.calculate_ingredient_cost(ing) for ing in ingredients)
        return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_unit_cost(total_cost: Decimal, yield_amount: int) -> Decimal:
        if yield_amount <= 0:
            raise ValueError("Yield must be positive")
        return (total_cost / Decimal(yield_amount)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    @staticmethod
    def calculate_final_price(unit_cost: Decimal, margin_percent: Decimal) -> Decimal:
        multiplier = Decimal('1') + (margin_percent / Decimal('100'))
        return (unit_cost * multiplier).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

def calculate_recipe_price(request: PriceCalculationRequest) -> PriceCalculationResponse:
    custo_total = PricingService.calculate_total_cost(request.ingredientes)
    custo_unitario = PricingService.calculate_unit_cost(custo_total, request.rendimento)
    preco_final_sugerido = PricingService.calculate_final_price(custo_unitario, request.margem_lucro)
    
    return PriceCalculationResponse(
        custo_total=custo_total,
        custo_unitario=custo_unitario,
        preco_final_sugerido=preco_final_sugerido
    )
```

---

## API Endpoint Design for RecipePricer

### Complete FastAPI Implementation

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Any

app = FastAPI(
    title="RecipePricer API",
    description="Calculate recipe costs and suggest final prices",
    version="1.0.0"
)

class Ingredient(BaseModel):
    nome: str = Field(..., min_length=1, example="Flour")
    custo_embalagem_fechada: Decimal = Field(..., gt=0, example="5.00")
    peso_embalagem_fechada: Decimal = Field(..., gt=0, example="1000")
    quantidade_usada: Decimal = Field(..., gt=0, example="250")

    @field_validator('custo_embalagem_fechada', 'peso_embalagem_fechada', 'quantidade_usada', mode='before')
    @classmethod
    def parse_decimal(cls, v: Any) -> Decimal:
        if isinstance(v, (int, float)):
            return Decimal(str(v))
        return Decimal(v)

class PriceCalculationRequest(BaseModel):
    ingredientes: List[Ingredient] = Field(..., min_length=1)
    rendimento: int = Field(..., gt=0, example=10)
    margem_lucro: Decimal = Field(..., ge=0, example="150")

class PriceCalculationResponse(BaseModel):
    custo_total: Decimal = Field(..., example="8.50")
    custo_unitario: Decimal = Field(..., example="0.85")
    preco_final_sugerido: Decimal = Field(..., example="2.13")

    class Config:
        json_encoders = {Decimal: lambda v: float(v) if v else 0.0}

@app.post("/calculate-price", response_model=PriceCalculationResponse)
async def calculate_price(request: PriceCalculationRequest):
    try:
        total = Decimal('0')
        for ing in request.ingredientes:
            cost = PricingCalculator.calculate_ingredient_cost(
                ing.quantidade_usada, ing.peso_embalagem_fechada, ing.custo_embalagem_fechada
            )
            total += cost
        
        custo_unitario = PricingCalculator.calculate_unit_cost(total, request.rendimento)
        preco_final = PricingCalculator.calculate_final_price(custo_unitario, request.margem_lucro)
        
        return PriceCalculationResponse(
            custo_total=total, custo_unitario=custo_unitario, preco_final_sugerido=preco_final
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

---

## Error Handling and Validation

### Custom Exceptions

```python
class PricingCalculationError(Exception):
    pass

class ZeroPackageWeightError(PricingCalculationError):
    pass

class ZeroYieldError(PricingCalculationError):
    pass

@app.post("/calculate-price")
async def calculate_price(request: PriceCalculationRequest):
    try:
        # ... calculations ...
        pass
    except ZeroPackageWeightError:
        raise HTTPException(status_code=400, detail="Package weight cannot be zero")
    except ZeroYieldError:
        raise HTTPException(status_code=400, detail="Recipe yield must be greater than zero")
    except PricingCalculationError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Division by Zero Handling

```python
from decimal import Decimal, DivisionByZero

def safe_divide(dividend: Decimal, divisor: Decimal, default: Decimal = Decimal('0')) -> Decimal:
    try:
        return dividend / divisor
    except DivisionByZero:
        return default

def calculate_ingredient_cost(
    quantity_used: Decimal, package_weight: Decimal, package_cost: Decimal
) -> Decimal:
    if package_weight == 0:
        raise ValueError("Package weight cannot be zero")
    cost = (quantity_used / package_weight) * package_cost
    return cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
```

---

## Testing Strategies

### Unit Tests for Decimal Calculations

```python
import pytest
from decimal import Decimal
from ..main import PricingCalculator, Ingredient

class TestPricingCalculator:
    def test_calculate_ingredient_cost_basic(self):
        result = PricingCalculator.calculate_ingredient_cost(
            quantity_used=Decimal('250'),
            package_weight=Decimal('1000'),
            package_cost=Decimal('5.00')
        )
        assert result == Decimal('1.25')
    
    def test_calculate_ingredient_cost_rounding(self):
        result = PricingCalculator.calculate_ingredient_cost(
            quantity_used=Decimal('333'),
            package_weight=Decimal('1000'),
            package_cost=Decimal('5.00')
        )
        assert result == Decimal('1.67')  # Rounded from 1.665
    
    def test_calculate_total_cost_multiple_ingredients(self):
        ingredients = [
            Ingredient(nome="Flour", custo_embalagem_fechada=Decimal('5.00'), peso_embalagem_fechada=Decimal('1000'), quantidade_usada=Decimal('250')),
            Ingredient(nome="Sugar", custo_embalagem_fechada=Decimal('3.00'), peso_embalagem_fechada=Decimal('500'), quantidade_usada=Decimal('100')),
        ]
        result = PricingCalculator.calculate_total_cost(ingredients)
        assert result == Decimal('2.10')
    
    def test_calculate_unit_cost(self):
        result = PricingCalculator.calculate_unit_cost(total_cost=Decimal('8.50'), yield_amount=10)
        assert result == Decimal('0.85')
    
    def test_calculate_final_price(self):
        result = PricingCalculator.calculate_final_price(unit_cost=Decimal('0.85'), margin_percent=Decimal('150'))
        # 0.85 * (1 + 150/100) = 0.85 * 2.5 = 2.125 -> 2.13
        assert result == Decimal('2.13')
```

### Integration Tests for API Endpoint

```python
from fastapi.testclient import TestClient

def test_calculate_price_endpoint():
    client = TestClient(app)
    
    response = client.post("/calculate-price", json={
        "ingredientes": [{
            "nome": "Flour",
            "custo_embalagem_fechada": "5.00",
            "peso_embalagem_fechada": "1000",
            "quantidade_usada": "250"
        }],
        "rendimento": 10,
        "margem_lucro": "150"
    })
    
    assert response.status_code == 200
    data = response.json()
    assert float(data['custo_total']) == 1.25
    assert float(data['custo_unitario']) == 0.125
    assert float(data['preco_final_sugerido']) == 0.31

def test_calculate_price_validation_error():
    client = TestClient(app)
    
    response = client.post("/calculate-price", json={
        "ingredientes": [],
        "rendimento": 10,
        "margem_lucro": "150"
    })
    
    assert response.status_code == 422
```

---

## Best Practices Summary

### 1. Decimal Best Practices

```python
# DO: Use string literals for Decimal creation
Decimal('0.1')  # Correct
Decimal(0.1)     # Incorrect - creates from float approximation

# DO: Quantize results for currency
result = (Decimal('1') / Decimal('3')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

# DO: Use Decimal('0') instead of 0 for initialization
total = Decimal('0')
```

### 2. Pydantic Best Practices

```python
# DO: Use field_validator for input conversion
@field_validator('field_name', mode='before')
def convert_input(cls, v):
    return Decimal(str(v)) if isinstance(v, float) else Decimal(v)

# DO: Set appropriate constraints
Field(..., gt=0, description="Positive value required")

# DO: Configure JSON encoders for clean output
class Config:
    json_encoders = {Decimal: lambda v: float(v)}
```

### 3. Business Logic Best Practices

```python
# DO: Separate business logic from API layer
# Create a service/class for calculations

# DO: Handle edge cases explicitly
# Zero division, empty lists, negative values

# DO: Use meaningful variable names matching domain language
# quantidade_usada vs qty, peso_embalagem_fechada vs pkg_weight
```

### 4. API Design Best Practices

```python
# DO: Use async def for endpoint handlers
# DO: Return consistent Decimal format
# DO: Include comprehensive error messages
# DO: Use response_model for automatic Swagger/OpenAPI documentation
```

---

## Complete Implementation Example

### main.py

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Any

app = FastAPI(title="RecipePricer API")

class Ingredient(BaseModel):
    nome: str = Field(..., min_length=1)
    custo_embalagem_fechada: Decimal = Field(..., gt=0)
    peso_embalagem_fechada: Decimal = Field(..., gt=0)
    quantidade_usada: Decimal = Field(..., gt=0)
    
    @field_validator('custo_embalagem_fechada', 'peso_embalagem_fechada', 'quantidade_usada', mode='before')
    @classmethod
    def ensure_decimal(cls, v: Any) -> Decimal:
        return Decimal(str(v)) if isinstance(v, float) else Decimal(v)

class PriceCalculationRequest(BaseModel):
    ingredientes: List[Ingredient] = Field(..., min_length=1)
    rendimento: int = Field(..., gt=0)
    margem_lucro: Decimal = Field(..., ge=0)

class PriceCalculationResponse(BaseModel):
    custo_total: float
    custo_unitario: float
    preco_final_sugerido: float

def calculate_ingredient_cost(quantity: Decimal, weight: Decimal, cost: Decimal) -> Decimal:
    return ((quantity / weight) * cost).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

@app.post("/calculate-price", response_model=PriceCalculationResponse)
async def calculate_price(request: PriceCalculationRequest):
    total_cost = sum(
        calculate_ingredient_cost(
            ing.quantidade_usada, ing.peso_embalagem_fechada, ing.custo_embalagem_fechada
        )
        for ing in request.ingredientes
    )
    
    unit_cost = (Decimal(total_cost) / Decimal(request.rendimento)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    final_price = (unit_cost * (Decimal('1') + request.margem_lucro / Decimal('100'))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return PriceCalculationResponse(
        custo_total=float(total_cost),
        custo_unitario=float(unit_cost),
        preco_final_sugerido=float(final_price)
    )
```

### Example Usage

```json
// Request
{
  "ingredientes": [
    {
      "nome": "Flour",
      "custo_embalagem_fechada": "5.00",
      "peso_embalagem_fechada": "1000",
      "quantidade_usada": "250"
    },
    {
      "nome": "Sugar",
      "custo_embalagem_fechada": "3.00",
      "peso_embalagem_fechada": "500",
      "quantidade_usada": "100"
    }
  ],
  "rendimento": 10,
  "margem_lucro": "150"
}

// Response
{
  "custo_total": 2.10,
  "custo_unitario": 0.21,
  "preco_final_sugerido": 0.53
}
```

---

## Conclusion

This research document covered:
1. Decimal type handling in Python for financial precision
2. Pydantic integration for Decimal validation and serialization
3. FastAPI endpoint patterns for pricing calculations
4. Rule of three implementation with proper error handling
5. Business logic patterns for modular, testable code
6. Testing strategies including unit and integration tests
7. Best practices for maintainable implementation

The key takeaways for RecipePricer:
- Always use string initialization for Decimal values
- Apply `quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)` for currency
- Validate package weights and quantities are positive
- Separate business logic from API layer
- Handle edge cases like division by zero explicitly

---

## Extended Patterns and Considerations

### Pattern for Percentage vs Multiplier Margin

The business requirement specifies `margem_lucro` as a percentage. Understanding the calculation:

```python
# If margem_lucro = 150% (meaning 150% above cost)
# preco_final = custo_unitario * (1 + 150/100) = custo_unitario * 2.5

# If margem_lucro = 50% (meaning 50% above cost)  
# preco_final = custo_unitario * (1 + 50/100) = custo_unitario * 1.5

# Margin interpretation example:
# custo_unitario = 0.85, margem_lucro = 150
# multiplier = 1 + (150/100) = 2.5
# preco_final = 0.85 * 2.5 = 2.125 -> quantize to 2.13
```

### Handling Large Numbers and Precision

```python
from decimal import Decimal, ROUND_HALF_UP, getcontext

# For large numbers, ensure sufficient precision
getcontext().prec = 10  # Adjust based on business needs

def calculate_large_recipe_cost(ingredients: List[Ingredient]) -> Decimal:
    """Handle recipes with many ingredients requiring high precision."""
    total = Decimal('0')
    for ing in ingredients:
        # Use intermediate precision for calculation
        cost = ((ing.quantidade_usada / ing.peso_embalagem_fechada) * ing.custo_embalagem_fechada)
        # Quantize intermediate results to avoid precision drift
        cost = cost.quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP)
        total += cost
    
    # Final result quantized to currency precision
    return total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
```

### Batch Processing Pattern

```python
from typing import List
from decimal import Decimal, ROUND_HALF_UP

async def calculate_multiple_recipes(recipes: List[PriceCalculationRequest]) -> List[PriceCalculationResponse]:
    """Process multiple recipes concurrently."""
    tasks = [calculate_price_async(recipe) for recipe in recipes]
    return await asyncio.gather(*tasks)

async def calculate_price_async(request: PriceCalculationRequest) -> PriceCalculationResponse:
    """Async version of price calculation for batch processing."""
    total = Decimal('0')
    for ing in request.ingredientes:
        cost = ((ing.quantidade_usada / ing.peso_embalagem_fechada) * ing.custo_embalagem_fechada)
        total += cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    unit_cost = (total / Decimal(request.rendimento)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    final_price = (unit_cost * (Decimal('1') + request.margem_lucro / Decimal('100'))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return PriceCalculationResponse(
        custo_total=float(total),
        custo_unitario=float(unit_cost),
        preco_final_sugerido=float(final_price)
    )
```

### Configuration with Environment Variables

```python
from decimal import Decimal
from pydantic import BaseSettings, Field

class PricingSettings(BaseSettings):
    default_profit_margin: Decimal = Decimal('100')
    currency_precision: int = 2
    max_ingredients_per_recipe: int = 100
    rounding_mode: str = 'ROUND_HALF_UP'
    
    class Config:
        env_file = '.env'

settings = PricingSettings()

def get_rounding_mode():
    from decimal import ROUND_HALF_UP, ROUND_HALF_EVEN
    return {'ROUND_HALF_UP': ROUND_HALF_UP, 'ROUND_HALF_EVEN': ROUND_HALF_EVEN}[settings.rounding_mode]
```

### Logging and Audit Trail

```python
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)

def calculate_with_logging(ingredient: Ingredient) -> Decimal:
    """Calculate with audit logging."""
    logger.info(f"Calculating cost for {ingredient.nome}: "
                f"qty={ingredient.quantidade_usada}, "
                f"weight={ingredient.peso_embalagem_fechada}, "
                f"cost={ingredient.custo_embalagem_fechada}")
    
    cost = ((ingredient.quantidade_usada / ingredient.peso_embalagem_fechada) * ingredient.custo_embalagem_fechada)
    result = cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    logger.info(f"Calculated proportional cost for {ingredient.nome}: {result}")
    return result
```

### Validation for Business Rules

```python
from pydantic import field_validator, model_validator
from decimal import Decimal

class Ingredient(BaseModel):
    nome: str
    custo_embalagem_fechada: Decimal
    peso_embalagem_fechada: Decimal
    quantidade_usada: Decimal

class PriceCalculationRequest(BaseModel):
    ingredientes: List[Ingredient] = Field(..., min_length=1)
    rendimento: int = Field(..., gt=0)
    margem_lucro: Decimal = Field(..., ge=0)
    
    @model_validator(mode='after')
    def validate_ingredients(self):
        """Cross-field validation for ingredients."""
        for ing in self.ingredientes:
            # Optional: Warn if quantity exceeds package weight
            if ing.quantidade_usada > ing.peso_embalagem_fechada:
                # Log warning or raise error based on business rules
                pass
        return self
```

### Type-Safe Service Pattern

```python
from typing import Protocol, runtime_checkable
from decimal import Decimal

@runtime_checkable
class PricingCalculator(Protocol):
    def calculate(self, request: PriceCalculationRequest) -> PriceCalculationResponse: ...

class DefaultPricingCalculator:
    def calculate(self, request: PriceCalculationRequest) -> PriceCalculationResponse:
        # Implementation here
        pass

class DiscountedPricingCalculator:
    """Alternative calculator with volume discounts."""
    def calculate(self, request: PriceCalculationRequest) -> PriceCalculationResponse:
        # Apply discounts based on quantity
        pass

# Dependency injection pattern
def get_pricing_calculator() -> PricingCalculator:
    return DefaultPricingCalculator()
```

### Metrics Collection

```python
from prometheus_client import Counter, Histogram
from decimal import Decimal

# Metrics
calculations_total = Counter('pricing_calculations_total', 'Total pricing calculations')
calculation_duration = Histogram('pricing_calculation_duration_seconds', 'Calculation duration')

@app.post("/calculate-price")
@calculation_duration.time()
async def calculate_price(request: PriceCalculationRequest):
    calculations_total.inc()
    # ... rest of implementation
```

### Retry Pattern for External Dependencies

```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=10))
async def fetch_ingredient_pricing(ingredient_id: str) -> Decimal:
    """Fetch pricing from external service with retry."""
    # External API call
    pass
```

---

## Mathematical Edge Cases

### Zero Values

```python
def handle_zero_values(ingredients: List[Ingredient]) -> Decimal:
    """Handle ingredients with zero costs or weights."""
    total = Decimal('0')
    for ing in ingredients:
        # Skip ingredients with zero cost (free ingredients)
        if ing.custo_embalagem_fechada == 0:
            continue
        
        # Protect against zero weight
        weight = ing.peso_embalagem_fechada if ing.peso_embalagem_fechada > 0 else Decimal('1')
        cost = ((ing.quantidade_usada / weight) * ing.custo_embalagem_fechada)
        total += cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    return total
```

### Negative Values

```python
def validate_non_negative(value: Decimal, field_name: str) -> Decimal:
    """Ensure value is non-negative."""
    if value < 0:
        raise ValueError(f"{field_name} cannot be negative")
    return value

# In Pydantic model:
@field_validator('custo_embalagem_fechada', 'quantidade_usada')
def validate_positive(cls, v):
    if v < 0:
        raise ValueError("Value must be non-negative")
    return v
```

### Very Small Decimals

```python
from decimal import Decimal

def handle_small_quantities(quantity: Decimal, weight: Decimal, cost: Decimal) -> Decimal:
    """Handle very small quantity ratios."""
    if quantity == Decimal('0'):
        return Decimal('0')
    
    ratio = quantity / weight
    # Handle scientific notation if needed
    cost = (ratio * cost).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return cost
```

---

## Response Serialization Options

### Option 1: Float Response (Default JSON-friendly)

```python
class PriceCalculationResponse(BaseModel):
    custo_total: float
    custo_unitario: float
    preco_final_sugerido: float
```

### Option 2: String Response (Precision preserved)

```python
class PriceCalculationResponse(BaseModel):
    custo_total: str
    custo_unitario: str
    preco_final_sugerido: str
    
    @field_serializer('custo_total', 'custo_unitario', 'preco_final_sugerido')
    def serialize_decimal(self, value: Decimal) -> str:
        return str(value.quantize(Decimal('0.01')))
```

### Option 3: Number Response (Mixed)

```python
class PriceCalculationResponse(BaseModel):
    custo_total: float
    custo_unitario: float
    preco_final_sugerido: float
    margem_aplicada: int  # Percentage as integer
```

---

## Final Notes

This research document provides a comprehensive foundation for implementing the RecipePricer API with:
- Proper Decimal handling for financial accuracy
- Clean Pydantic models for input validation
- FastAPI endpoint design following best practices
- Rule of three calculation patterns with error handling
- Testing strategies for quality assurance
- Extensible patterns for future enhancements