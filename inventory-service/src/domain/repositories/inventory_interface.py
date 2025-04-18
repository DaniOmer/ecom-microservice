from abc import ABC, abstractmethod
from src.domain.entities import Inventory

class InventoryInterface(ABC):
    @abstractmethod
    def get_inventory_by_uid(self, product_uid: str) -> Inventory:
        pass

    @abstractmethod
    def create_inventory(self, inventory: Inventory) -> Inventory:
        pass

    @abstractmethod
    def update_inventory(self, inventory: Inventory) -> None:
        pass

    @abstractmethod
    def reserve_inventory(self, product_uid: str, amount: int) -> None:
        pass

    @abstractmethod
    def release_inventory(self, product_uid: str, amount: int) -> None:
        pass
