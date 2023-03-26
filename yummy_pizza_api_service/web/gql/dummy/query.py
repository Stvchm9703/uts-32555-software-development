from typing import List

import strawberry

from yummy_pizza_api_service.db.dao.dummy_dao import DummyDAO
from yummy_pizza_api_service.web.gql.dummy.schema import DummyModelDTO


@strawberry.type
class Query:
    """Query to interact with dummies."""

    @strawberry.field(description="Get all dummies")
    async def get_dummy_models(
        self,
        limit: int = 15,
        offset: int = 0,
    ) -> List[DummyModelDTO]:
        """
        Retrieves all dummy objects from database.

        :param limit: limit of dummy objects, defaults to 10.
        :param offset: offset of dummy objects, defaults to 0.
        :return: list of dummy obbjects from database.
        """
        dao = DummyDAO()
        return await dao.get_all_dummies(limit=limit, offset=offset)  # type: ignore
