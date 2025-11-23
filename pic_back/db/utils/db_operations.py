from typing import List, Protocol


class DbOperations(Protocol):  # pragma: no cover
    @classmethod
    def delete(cls, category_name: str) -> List[int]:
        pass

    @classmethod
    def exists(cls, category_name: str) -> bool:
        pass
