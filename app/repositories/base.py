from typing import Any, Generic, TypeVar

from beanie import Document

DocumentType = TypeVar("DocumentType", bound=Document)


class BaseRepository(Generic[DocumentType]):
    def __init__(self, model: type[DocumentType]) -> None:
        self.model = model

    async def create(
        self,
        data: DocumentType | dict[str, Any],
    ) -> DocumentType:
        if isinstance(data, self.model):
            document= data
        else:
            document =self.model(**data)
            
        await document.insert()
        return document

    async def get_by_id(
        self,
        document_id: str,
    ) -> DocumentType | None:
        return await self.model.get(document_id)

    async def get_all(self) -> list[DocumentType]:
        return await self.model.find_all().to_list()

    async def update(
        self,
        document: DocumentType,
        data: dict[str, Any],
    ) -> DocumentType:
        for key, value in data.items():
            setattr(document, key, value)

        await document.save()
        return document

    async def delete(
        self,
        document: DocumentType,
    ) -> None:
        await document.delete()