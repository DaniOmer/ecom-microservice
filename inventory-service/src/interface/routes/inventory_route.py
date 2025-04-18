from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database import DatabaseFactory
from src.application.services import InventoryService
from src.infrastructure.repositories import InventoryRepository
from src.infrastructure.schemas import (
    InventoryCreateSchema,
    InventoryUpdateSchema,
    InventoryReserveSchema,
    InventoryReleaseSchema
)

router = APIRouter(prefix="/inventory")
db_instance = DatabaseFactory.create_strategy('sqlalchemy').get_session

@router.post("/", status_code=201)
async def create_inventory(
    inventory: InventoryCreateSchema, session: AsyncSession = Depends(db_instance)):
    inventory_service = InventoryService(InventoryRepository(session))
    created_inventory = await inventory_service.create_inventory(inventory)
    return {
        "message": "Inventory created",
        "inventory": {
            "id": created_inventory.id,
            "product_uid": created_inventory.product_uid,
            "quantity_available": created_inventory.quantity_available,
            "reserved_quantity": created_inventory.reserved_quantity
        }
    }

@router.get("/{product_uid}")
async def get_inventory(product_uid: str, session: AsyncSession = Depends(db_instance)):
    inventory_service = InventoryService(InventoryRepository(session))
    inventory = await inventory_service.get_inventory_by_uid(product_uid)
    return inventory

@router.put("/{product_uid}")
async def update_inventory(product_uid: str, inventory: InventoryUpdateSchema, session: AsyncSession = Depends(db_instance)):
    inventory_service = InventoryService(InventoryRepository(session))
    await inventory_service.update_inventory(product_uid, inventory)
    return {"message": "Inventory updated"}

@router.post("/reserve")
async def reserve_inventory(inventory: InventoryReserveSchema, session: AsyncSession = Depends(db_instance)):
    inventory_service = InventoryService(InventoryRepository(session))
    await inventory_service.reserve_inventory(inventory.product_uid, inventory.amount)
    return {"message": "Inventory reserved"}

@router.post("/release")
async def release_inventory(inventory: InventoryReleaseSchema, session: AsyncSession = Depends(db_instance)):
    inventory_service = InventoryService(InventoryRepository(session))
    await inventory_service.release_inventory(inventory.product_uid, inventory.amount)
    return {"message": "Inventory released"}
