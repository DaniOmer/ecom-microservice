from abc import ABC, abstractmethod

class DatabaseStrategy(ABC):
    @abstractmethod
    def get_instance(cls):
        pass
    
    @abstractmethod
    def get_session(cls):
        pass
    
    @abstractmethod
    def get_engine(cls):
        pass    