from typing import List, Protocol


class DbOperations(Protocol):
    @classmethod
    def delete(cls, category_name: str) -> List[int]:
        pass

    @classmethod
    def exists(cls, category_name: str) -> bool:
        pass

    # @classmethod
    # def get_all(cls) -> List[BaseModel]:
    #     pass
