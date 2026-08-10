from typing import Any, Generic, TypeVar

from beanie import Document

from app.schemas.pagination import (
    PaginatedResponse,
    PaginationResponse,
)

DocumentType = TypeVar("DocumentType", bound=Document)


class BaseRepository(Generic[DocumentType]):
    def __init__(self, model: type[DocumentType]) -> None:
        self.model = model

    async def create(
        self,
        data: DocumentType | dict[str, Any],
    ) -> DocumentType:
        if isinstance(data, self.model):
            document = data
        else:
            document = self.model(**data)

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

    async def get_paginated(
            self,
            page: int,
            page_size: int,
    ) -> PaginatedResponse:
        skip = (page - 1) * page_size

        total = await self.model.count()

        documents = (
            await self.model.find_all()
            .skip(skip)
            .limit(page_size)
            .to_list()
        )

        pages = (total + page_size - 1) // page_size

        return PaginatedResponse(
            items=documents,
            pagination=PaginationResponse(
                page=page,
                page_size=page_size,
                total=total,
                pages=pages
            )
        )
        
        
