from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlalchemy import delete, desc, update

from api.models.session import SessionModel
from api.repositories.base import BaseRepository


class SessionRepository(BaseRepository[SessionModel]):
    async def create(self, *, metadata: dict | None = None) -> SessionModel:
        session = SessionModel(
            id=uuid4(),
            metadata_=(metadata or {}),
        )
        return await self.add(session)

    async def get_by_id(self, session_id: UUID) -> SessionModel | None:
        statement = self.select_model(SessionModel).where(SessionModel.id == session_id)
        return await self.execute_one_or_none(statement)

    async def update_last_active(self, session_id: UUID) -> SessionModel | None:
        await self.session.execute(
            update(SessionModel)
            .where(SessionModel.id == session_id)
            .values(last_active_at=datetime.now(timezone.utc))
        )
        await self.session.flush()
        return await self.get_by_id(session_id)

    async def list_inactive_before(self, cutoff: datetime) -> list[SessionModel]:
        statement = (
            self.select_model(SessionModel)
            .where(SessionModel.last_active_at < cutoff)
            .order_by(desc(SessionModel.last_active_at))
        )
        return list(await self.execute_all(statement))

    async def delete_by_id(self, session_id: UUID) -> bool:
        result = await self.session.execute(
            delete(SessionModel).where(SessionModel.id == session_id)
        )
        await self.session.flush()
        return result.rowcount > 0
