import requests
import re
import httpx
from typing import Optional
from fastapi import HTTPException, status

from app.schemas.address_schema import AddressBaseSchema, AddressCreateSchema


class CEPNotFoundError(Exception):
    pass

REQUIRED_FIELDS = [
    "state",
    "city",
    "neighborhood",
    "street",
    "number"
]


def _build_address(address: AddressCreateSchema, cep_data: Optional[dict]) -> AddressBaseSchema:
    data = {
        "zip_code": address.zip_code,
        "country": address.country,
        "state": address.state,
        "city": address.city,
        "neighborhood": address.neighborhood,
        "street": address.street,
        "number": address.number,
        "complement": address.complement,
        "latitude": address.latitude,
        "longitute": address.longitude
    }
    if cep_data:
        data.update({
            "state": cep_data.get("state") or data["state"],
            "city": cep_data.get("city") or data["city"],
            "neighborhood": cep_data.get("neighborhood") or data["neighborhood"],
            "street": cep_data.get("street") or data["street"]
        })
 
    missing = [f for f in REQUIRED_FIELDS if not data.get(f)]
    if missing:
        raise ValueError(
            f"Incomplete address. Missing fields. {', '.join(missing)}"
        )

    return AddressBaseSchema(**data)
     


async def resolve_address_input_async(address: AddressCreateSchema) -> AddressBaseSchema:
    cep_data = None

    try:
        cep_data = await get_address_from_cep_async(address.zip_code)
    except CEPNotFoundError:
        pass
    return _build_address(address, cep_data)

def resolve_address_input(address: AddressCreateSchema) -> AddressBaseSchema:
    cep_data = None

    try:
        cep_data = get_address_from_cep(address.zip_code)
    except Exception:
        cep_data = None

    return _build_address(address, cep_data)


def get_address_from_cep(cep: str) -> dict:
    cep = normalize_cep(cep)

    response = requests.get(
        f"https://viacep.com.br/ws/{cep}/json/",
        timeout = 5
    )

    if response.status_code != status.HTTP_200_OK:
        raise CEPNotFoundError("Error consulting zip code")

    data = response.json()

    if data.get("erro"):
        raise CEPNotFoundError("Zip code not found")

    return {
        "zip_code": cep,
        "street": data.get("logradouro"),
        "neighborhood": data.get("bairro"),
        "city": data.get("localidade"),
        "state": data.get("uf"),
        "country": "BR"
    }

async def get_address_from_cep_async(cep: str) -> dict:
    cep = normalize_cep(cep)

    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(
            f"https://viacep.com.br/ws/{cep}/json/"
        )
    response.raise_for_status()

    data = response.json()

    if data.get("erro"):
        raise CEPNotFoundError("Zip code not found")

    return {
        "zip_code": cep,
        "street": data.get("logradouro"),
        "neighborhood": data.get("bairro"),
        "city": data.get("localidade"),
        "state": data.get("uf"),
        "country": "BR"
    }

def normalize_cep(cep: str) -> str:
    if not cep:
        raise CEPNotFoundError("Invalid BR zip-code 'CEP'")
    
    digits = re.sub(r"\D","",cep)

    if len(digits) != 8:
        raise CEPNotFoundError("Invalid BR zip-code 'CEP'")
    
    return digits

