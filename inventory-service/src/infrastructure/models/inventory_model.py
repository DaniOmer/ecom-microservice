from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime

from src.domain.entities import Inventory
from src.infrastructure.models.base_model import Base

class InventoryModel(Base):
    __tablename__ = "inventories"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    product_uid = Column(String, nullable=False)
    quantity_available = Column(Integer, nullable=False)
    reserved_quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)

    @staticmethod
    def from_entity(inventory):
        return InventoryModel(
            id=inventory.id if hasattr(inventory, 'id') and inventory.id is not None else None,
            product_uid=inventory.product_uid,
            quantity_available=inventory.quantity_available,
            reserved_quantity=inventory.reserved_quantity,
            created_at=inventory.created_at,
            updated_at=inventory.updated_at,
        )

    def to_entity(self):
        return Inventory(
            id=self.id,
            product_uid=self.product_uid,
            quantity_available=self.quantity_available,
            reserved_quantity=self.reserved_quantity,
            created_at=self.created_at, 
            updated_at=self.updated_at,
        )
