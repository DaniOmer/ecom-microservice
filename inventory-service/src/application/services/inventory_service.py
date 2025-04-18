from datetime import datetime, timezone
from src.domain.entities import Inventory
from src.domain.repositories import InventoryInterface
from src.infrastructure.schemas import InventoryCreateSchema, InventoryUpdateSchema

class InventoryService:
    def __init__(self, inventory_repository: InventoryInterface):
        self.inventory_repository = inventory_repository

    async def get_inventory_by_uid(self, product_uid: str) -> Inventory:
        return await self.inventory_repository.get_inventory_by_uid(product_uid)

    async def create_inventory(self, inventory_schema: InventoryCreateSchema) -> Inventory:
        inventory = Inventory(
            product_uid=inventory_schema.product_uid,
            quantity_available=inventory_schema.quantity_available,
            reserved_quantity=inventory_schema.reserved_quantity
        )
        return await self.inventory_repository.create_inventory(inventory)

    async def update_inventory(self, product_uid: str, inventory_schema: InventoryUpdateSchema) -> None:
        # First get the current inventory
        current_inventory = await self.inventory_repository.get_inventory_by_uid(product_uid)
        
        # Update only the quantity_available field
        current_inventory.quantity_available = inventory_schema.quantity_available
        current_inventory.updated_at = datetime.now(timezone.utc)
        
        # Save the updated inventory
        await self.inventory_repository.update_inventory(current_inventory)

    async def reserve_inventory(self, product_uid: str, amount: int) -> None:
        await self.inventory_repository.reserve_inventory(product_uid, amount)

    async def release_inventory(self, product_uid: str, amount: int) -> None:
        await self.inventory_repository.release_inventory(product_uid, amount)
