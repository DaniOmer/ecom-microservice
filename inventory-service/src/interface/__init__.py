from fastapi import FastAPI

from src.interface.routes.inventory_route import router as inventory_route

app = FastAPI(
    title="Inventory Service",
    description="This is Inventory Service.",
    version="1.0.0",
    contact={
        "name": "Inventory Service Team",
        "url": "https://inventory-service.com",
        "email": "inventory-service@infos.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Routers
app.include_router(inventory_route)
