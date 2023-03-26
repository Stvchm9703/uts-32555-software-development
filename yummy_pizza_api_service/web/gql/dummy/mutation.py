import strawberry

from yummy_pizza_api_service.db.dao.dummy_dao import DummyDAO


@strawberry.type
class Mutation:
    """Mutations for dummies."""

    @strawberry.mutation(description="Create dummy object in a database")
    async def create_dummy_model(
        self,
        name: str,
    ) -> str:
        """
        Creates dummy model in a database.

        :param name: name of a dummy.
        :return: name of a dummt model.
        """
        dao = DummyDAO()
        await dao.create_dummy_model(name=name)
        return name
