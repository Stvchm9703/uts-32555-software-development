from fastapi.routing import APIRouter

from yummy_pizza_api_service.web.api import docs, dummy, echo, monitoring, product, order

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(echo.router, prefix="/echo", tags=["echo"])
api_router.include_router(dummy.router, prefix="/dummy", tags=["dummy"])
api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(order.router, prefix="/order", tags=["order"])
