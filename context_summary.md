# Context Summary: RecipePricer API

## Project Overview
- **Project Name**: RecipePricer
- **Primary Technology Stack**: FastAPI, Python, Pydantic, asyncio
- **Project Type**: REST API for recipe cost calculation and pricing
- **Source Code Directory**: /root/recipepricer (to be created)
- **Key Dependencies**: fastapi, pydantic, uvicorn, python-decouple (optional)

## Task-Specific Context

### Current Task
Create a FastAPI RecipePricer application with a POST /calculate-price endpoint that calculates the cost and suggested price for recipes based on ingredient packaging costs, yield, and profit margin.

### Core Business Requirements

#### Requirement 1: Ingredient Fields
Each ingredient in the recipe must have the following fields:
- **nome** (string): Name of the ingredient
- **custo_embalagem_fechada** (decimal): Cost of the sealed/closed packaging
- **peso_embalagem_fechada** (decimal): Weight/volume of the sealed packaging
- **quantidade_usada** (decimal): Amount of ingredient used in the recipe

#### Requirement 2: Recipe Yield
- **rendimento** (integer): Number of units the recipe produces
- This represents how many portions/servings/items the recipe yields
- Used to calculate per-unit costs

#### Requirement 3: Profit Margin
- **margem_lucro** (decimal/percentage): Profit margin percentage (e.g., 150%)
- This indicates how much above cost the final price should be
- A 150% margin means the price is 150% above the cost (or 2.5x multiplier: 100% cost + 150% profit)

#### Requirement 4: Return Values
The API response must include:
- **custo_total**: Total cost of all ingredients for the complete recipe
- **custo_unitario**: Cost per individual unit (custo_total / rendimento)
- **preco_final_sugerido**: Suggested final price per unit (custo_unitario * (1 + margem_lucro/100))

#### Requirement 5: Proportional Cost Calculation (Regra de Três / Rule of Three)
Calculate ingredient cost based on proportion used:
- Formula: `custo_ingrediente = (quantidade_usada / peso_embalagem_fechada) * custo_embalagem_fechada`
- This determines how much of the packaged ingredient's cost applies to the amount used
- Sum all ingredient costs to get the total recipe cost

#### Requirement 6: Technical Implementation Requirements
- **Async code**: Use asyncio patterns where appropriate
- **Pydantic validation**: Validate all input data using Pydantic models
- **Decimal precision**: Use Decimal type with ROUND_HALF_UP rounding for financial calculations
- **FastAPI endpoint**: POST /calculate-price

## API Design

### Request Model Structure
```python
class Ingredient:
    nome: str
    custo_embalagem_fechada: Decimal
    peso_embalagem_fechada: Decimal
    quantidade_usada: Decimal

class PriceCalculationRequest:
    ingredientes: List[Ingredient]
    rendimento: int
    margem_lucro: Decimal

### Response Model Structure
```python
class PriceCalculationResponse:
    custo_total: Decimal
    custo_unitario: Decimal
    preco_final_sugerido: Decimal
```

## Business Logic Flow

1. **Input Validation**: Validate all ingredient fields and recipe parameters
2. **Per-Ingredient Cost Calculation**: Apply regra de três for each ingredient
3. **Total Cost**: Sum all individual ingredient costs
4. **Unit Cost**: Divide total cost by recipe yield
5. **Final Price**: Apply profit margin to unit cost
6. **Return Results**: Provide all three calculated values

## Constraints & Considerations

- All monetary values must use Decimal for precision
- Profit margin of 150% means price = cost * (1 + 1.50) = cost * 2.5
- Recipe yield must be a positive integer greater than 0
- Packaging weight and used quantity must be positive decimals
- Empty ingredient list should be handled gracefully
- All fields are required (no optional values)

## Example Calculation

**Recipe**: 10 units of a dessert
**Profit Margin**: 150%

**Ingredient**: Flour
- Package cost: R$ 5.00
- Package weight: 1000g
- Amount used: 250g

**Calculation**:
- flour_cost = (250 / 1000) * 5.00 = R$ 1.25
- If total ingredients cost = R$ 8.50
- custo_total = R$ 8.50
- custo_unitario = 8.50 / 10 = R$ 0.85
- preco_final_sugerido = 0.85 * (1 + 1.50) = R$ 2.13

## Technical Specifications

- Python 3.8+ required for proper async support
- FastAPI for automatic API documentation (Swagger/OpenAPI)
- Pydantic for request/response model validation
- Decimal with ROUND_HALF_UP for all financial arithmetic
- Async def endpoints for better performance under load