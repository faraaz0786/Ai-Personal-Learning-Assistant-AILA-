from collections.abc import Sequence
from typing import Generic, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.timing import timing_tracker


ModelT = TypeVar("ModelT")


class BaseRepository(Generic[ModelT]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, instance: ModelT) -> ModelT:
        with timing_tracker.measure("db"):
            self.session.add(instance)
            await self.session.flush()
            try:
                await self.session.refresh(instance)
            except Exception as e:
                import logging
                logging.getLogger(__name__).warning(f"Could not refresh instance: {e}")
            return instance

    async def delete(self, instance: ModelT) -> None:
        with timing_tracker.measure("db"):
            await self.session.delete(instance)
            await self.session.flush()

    async def execute_one_or_none(self, statement: Select[tuple[ModelT]]) -> ModelT | None:
        with timing_tracker.measure("db"):
            result = await self.session.execute(statement)
            return result.scalar_one_or_none()

    async def execute_all(self, statement: Select[tuple[ModelT]]) -> Sequence[ModelT]:
        with timing_tracker.measure("db"):
            result = await self.session.execute(statement)
            return result.scalars().all()

    @staticmethod
    def select_model(model: type[ModelT]) -> Select[tuple[ModelT]]:
        return select(model)
