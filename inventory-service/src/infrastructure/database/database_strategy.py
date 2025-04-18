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
    
    @abstractmethod
    def get_session_with_retry(cls, max_retries=5, retry_delay=1):
        pass
