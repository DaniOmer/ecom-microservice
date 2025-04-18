from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories import InventoryInterface
from src.domain.entities import Inventory
from src.infrastructure.models.inventory_model import InventoryModel
from datetime import datetime, timezone

class InventoryRepository(InventoryInterface):
    def __init__(self, db: AsyncSession = None):
        self.db = db

    async def get_inventory_by_uid(self, product_uid: str) -> Inventory:
        from sqlalchemy import select
        
        query = select(InventoryModel).where(InventoryModel.product_uid == product_uid)
        result = await self.db.execute(query)
        inventory_model = result.scalars().first()
        
        if not inventory_model:
            raise ValueError(f"Inventory not found for product_uid: {product_uid}")
            
        return inventory_model.to_entity()

    async def create_inventory(self, inventory: Inventory) -> Inventory:
        inventory_model = InventoryModel.from_entity(inventory)
        self.db.add(inventory_model)
        try:
            await self.db.flush()
            # Get the generated ID and update the entity
            inventory.id = inventory_model.id
            await self.db.commit()
            return inventory
        except Exception as e:
            await self.db.rollback()
            raise e

    async def update_inventory(self, inventory: Inventory) -> None:
        from sqlalchemy import select
        
        query = select(InventoryModel).where(InventoryModel.product_uid == inventory.product_uid)
        result = await self.db.execute(query)
        inventory_model = result.scalars().first()
        
        if not inventory_model:
            raise ValueError(f"Inventory not found for product_uid: {inventory.product_uid}")
            
        inventory_model.quantity_available = inventory.quantity_available
        inventory_model.reserved_quantity = inventory.reserved_quantity
        inventory_model.updated_at = inventory.updated_at
        
        await self.db.commit()

    async def reserve_inventory(self, product_uid: str, amount: int) -> None:
        from sqlalchemy import select
        
        query = select(InventoryModel).where(InventoryModel.product_uid == product_uid)
        result = await self.db.execute(query)
        inventory_model = result.scalars().first()
        
        if not inventory_model:
            raise ValueError(f"Inventory not found for product_uid: {product_uid}")
            
        if inventory_model.quantity_available < amount:
            raise ValueError(f"Not enough inventory available. Available: {inventory_model.quantity_available}, Requested: {amount}")
            
        inventory_model.quantity_available -= amount
        inventory_model.reserved_quantity += amount
        inventory_model.updated_at = datetime.now(timezone.utc)
        
        await self.db.commit()

    async def release_inventory(self, product_uid: str, amount: int) -> None:
        from sqlalchemy import select
        
        query = select(InventoryModel).where(InventoryModel.product_uid == product_uid)
        result = await self.db.execute(query)
        inventory_model = result.scalars().first()
        
        if not inventory_model:
            raise ValueError(f"Inventory not found for product_uid: {product_uid}")
            
        if inventory_model.reserved_quantity < amount:
            raise ValueError(f"Not enough reserved inventory. Reserved: {inventory_model.reserved_quantity}, Requested: {amount}")
            
        inventory_model.quantity_available += amount
        inventory_model.reserved_quantity -= amount
        inventory_model.updated_at = datetime.now(timezone.utc)
        
        await self.db.commit()
