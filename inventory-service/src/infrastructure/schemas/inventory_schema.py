from pydantic import BaseModel

class InventoryCreateSchema(BaseModel):
    product_uid: str
    quantity_available: int
    reserved_quantity: int = 0

class InventoryUpdateSchema(BaseModel):
    product_uid: str
    quantity_available: int

class InventoryReserveSchema(BaseModel):
    product_uid: str
    amount: int

class InventoryReleaseSchema(BaseModel):
    product_uid: str
    amount: int



