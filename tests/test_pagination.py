from unittest.mock import AsyncMock, MagicMock

import pytest

from app.repositories.base import BaseRepository


class TestDocument:
    pass


@pytest.mark.anyio
async def test_get_paginated_first_page():
    repository = BaseRepository(TestDocument)

    documents = [
        MagicMock(id="1"),
        MagicMock(id="2"),
    ]

    mock_query = MagicMock()
    mock_query.skip.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.to_list = AsyncMock(return_value=documents)

    repository.model.count = AsyncMock(return_value=5)
    repository.model.find_all = MagicMock(return_value=mock_query)

    result = await repository.get_paginated(
        page=1,
        page_size=2,
    )

    assert result.items == documents
    assert result.pagination.page == 1
    assert result.pagination.page_size == 2
    assert result.pagination.total == 5
    assert result.pagination.pages == 3

    mock_query.skip.assert_called_once_with(0)
    mock_query.limit.assert_called_once_with(2)


@pytest.mark.anyio
async def test_get_paginated_second_page():
    repository = BaseRepository(TestDocument)

    documents = [
        MagicMock(id="3"),
        MagicMock(id="4"),
    ]

    mock_query = MagicMock()
    mock_query.skip.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.to_list = AsyncMock(return_value=documents)

    repository.model.count = AsyncMock(return_value=5)
    repository.model.find_all = MagicMock(return_value=mock_query)

    result = await repository.get_paginated(
        page=2,
        page_size=2,
    )

    assert result.items == documents
    assert result.pagination.page == 2
    assert result.pagination.page_size == 2
    assert result.pagination.total == 5
    assert result.pagination.pages == 3

    mock_query.skip.assert_called_once_with(2)
    mock_query.limit.assert_called_once_with(2)


@pytest.mark.anyio
async def test_get_paginated_empty_result():
    repository = BaseRepository(TestDocument)

    mock_query = MagicMock()
    mock_query.skip.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.to_list = AsyncMock(return_value=[])

    repository.model.count = AsyncMock(return_value=0)
    repository.model.find_all = MagicMock(return_value=mock_query)

    result = await repository.get_paginated(
        page=1,
        page_size=20,
    )

    assert result.items == []
    assert result.pagination.page == 1
    assert result.pagination.page_size == 20
    assert result.pagination.total == 0
    assert result.pagination.pages == 0
