"""FastAPI router for RecipePricer endpoint."""

from fastapi import APIRouter, status

from app.models import RecipeCalculateRequest, RecipeCalculateResponse
from app.services.pricing_service import PricingService

router = APIRouter()
pricing_service = PricingService()


@router.post(
    "/calculate-price",
    response_model=RecipeCalculateResponse,
    status_code=status.HTTP_200_OK,
    summary="Calculate recipe pricing",
    description="Calculates total cost, unit cost, and suggested selling price based on ingredients",
)
async def calculate_price(request: RecipeCalculateRequest) -> RecipeCalculateResponse:
    """Calculate recipe pricing with yield and profit margin."""
    return await pricing_service.calculate_price(request)