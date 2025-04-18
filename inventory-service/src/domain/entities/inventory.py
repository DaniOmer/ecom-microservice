from datetime import datetime, timezone
from typing import Optional

class Inventory:
    def __init__(
        self,
        product_uid: str,
        quantity_available: int,
        reserved_quantity: int = 0,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        id: Optional[int] = None,
    ):
        self.id = id
        self.product_uid = product_uid
        self.quantity_available = quantity_available
        self.reserved_quantity = reserved_quantity
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def reserve(self, amount: int):
        if self.quantity_available < amount:
            raise ValueError("Not enough inventory to reserve")
        self.quantity_available -= amount
        self.reserved_quantity += amount
        self.updated_at = datetime.now(timezone.utc)

    def release(self, amount: int):
        if self.reserved_quantity < amount:
            raise ValueError("Cannot release more than reserved")
        self.quantity_available += amount
        self.reserved_quantity -= amount
        self.updated_at = datetime.now(timezone.utc)
