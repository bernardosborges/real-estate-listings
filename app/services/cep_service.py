import requests
import re
import httpx
from typing import Optional

from app.schemas.address_schema import AddressBaseSchema, AddressCreateSchema
from app.core.exceptions.address_exceptions import CEPInvalid, CEPNotFound, AddressIncomplete

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
        "longitude": address.longitude
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
        raise AddressIncomplete(
            f"Incomplete address. Missing fields. {', '.join(missing)}"
        )

    return AddressBaseSchema(**data)
     


async def resolve_address_input_async(address: AddressCreateSchema) -> AddressBaseSchema:
    cep_data = None

    try:
        cep_data = await get_address_from_cep_async(address.zip_code)
    except CEPNotFound:
        pass
    return _build_address(address, cep_data)

def resolve_address_input(address: AddressCreateSchema) -> AddressBaseSchema:
    cep_data = None

    try:
        cep_data = get_address_from_cep(address.zip_code)
    except CEPNotFound:
        cep_data = None

    return _build_address(address, cep_data)


def get_address_from_cep(cep: str) -> dict:
    cep = normalize_cep(cep)

    try:
        response = requests.get(
            f"https://viacep.com.br/ws/{cep}/json/",
            timeout = 5
        )
    except requests.RequestException:
        raise CEPNotFound(cep)

    if response.status_code != 200:
        raise CEPNotFound(cep)

    data = response.json()

    if data.get("erro"):
        raise CEPNotFound(cep)

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

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(
                f"https://viacep.com.br/ws/{cep}/json/"
            )
    except httpx.RequestError:
        raise CEPNotFound(cep)

    if response.status_code != 200:
        raise CEPNotFound(cep)

    data = response.json()

    if data.get("erro"):
        raise CEPNotFound(cep)

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
        raise CEPInvalid("CEP is required")
    
    digits = re.sub(r"\D","",cep)

    if len(digits) != 8:
        raise CEPInvalid("CEP must have 8 digits")
    
    return digits

