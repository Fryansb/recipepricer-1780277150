# Development Plan - RecipePricer API

## Task: Crie RecipePricer API com endpoint POST /calculate-price

## Business Requirements Checklist (MUST verify all)
- [x] Ingredient: nome, custo_embalagem_fechada, peso_embalagem_fechada, quantidade_usada
- [x] Rendimento da receita (units produced)
- [x] Margem de lucro (% porcentagem)
- [x] Retornar: custo_total, custo_unitario, preco_final_sugerido
- [x] Cálculo regra de três para cada ingrediente
- [x] Async + Pydantic + Decimal ROUND_HALF_UP

## Atomized Development Tasks

### Task 2.1.1: Project Structure
- [ ] Create app/, tests/, WORKSPACE/ directories
- [ ] Create __init__.py files
- Est. time: 5 min

### Task 2.1.2: pyproject.toml
- [ ] FastAPI, uvicorn, pydantic dependencies
- [ ] pytest-asyncio configuration
- Est. time: 5 min

### Task 2.2.1: Ingredient Model
- [ ] ingredient_name: str
- [ ] custo_embalagem_fechada: Decimal (positive)
- [ ] peso_embalagem_fechada: Decimal (positive)
- [ ] quantidade_usada: Decimal (non-negative)
- Est. time: 10 min

### Task 2.2.2: Recipe Request Model
- [ ] ingredients: List[IngredientInput]
- [ ] rendimento: int (units produced)
- [ ] margem_lucro: Decimal (percentage, ex: 150 = 150%)
- Est. time: 10 min

### Task 2.2.3: Response Model
- [ ] custo_total: Decimal
- [ ] custo_unitario: Decimal
- [ ] preco_final_sugerido: Decimal
- [ ] ingredient_costs: List with breakdown
- Est. time: 10 min

### Task 2.3.1: Pricing Service
- [ ] calculate_ingredient_cost using rule of three: (quantidade / peso) * custo
- [ ] calculate_total_cost (sum all ingredients)
- [ ] calculate_unit_cost (total / rendimento)
- [ ] calculate_suggested_price (unit_cost * (1 + margem/100))
- Est. time: 15 min

### Task 2.4.1: FastAPI Router
- [ ] POST /calculate-price endpoint
- [ ] Uses PricingService
- [ ] Returns RecipeCalculateResponse
- Est. time: 10 min

### Task 2.5.x: Tests
- [ ] test_ingredient_cost_rule_of_three
- [ ] test_rendimento_calculation
- [ ] test_margem_lucro_calculation
- [ ] test_all_return_values
- Est. time: 20 min

### Task 2.6.0: Business Requirements Validation
- [ ] Run validate_business_requirements.py
- [ ] ALL 6 requirements must pass
- Est. time: 5 min