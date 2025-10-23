from fastapi import APIRouter

from .product import router as router_product

all_routers = APIRouter()

all_routers.include_router(router=router_product)