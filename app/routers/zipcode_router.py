from fastapi import APIRouter, HTTPException, status, Security

from app.core.oauth2 import get_current_user
from app.services.cep_service import get_address_from_cep_async
from app.models.user_model import UserModel
from app.schemas.address_schema import AddressLookupSchema

from app.core.config import settings

router = APIRouter(prefix=f"{settings.API_PREFIX}/cep", tags=["Zip_code"])


# -----------------------------------------------
# ENDPOINT - GET CEP
# -----------------------------------------------

@router.get(
        "/{zip_code}",
        response_model=AddressLookupSchema ,
        summary="Get address from a CEP",
        description="Returns address data from ViaCEP (authenticated users only)"
)
async def lookup_cep_endpoint(
    zip_code: str,
    current_user: UserModel = Security(get_current_user)
):
    try:
        return await get_address_from_cep_async(zip_code)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CEP not found")