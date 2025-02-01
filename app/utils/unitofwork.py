from abc import ABC, abstractmethod

from app.db.database import async_session_maker
from app.repositories.user_repo import UserRepository


class IUnitOfWork(ABC):

    @abstractmethod
    def __init__(self):
        ...

    @abstractmethod
    async def __aenter__(self):
        ...

    @abstractmethod
    async def __aexit__(self, *args):
        ...

    @abstractmethod
    async def commit(self):
        ...

    @abstractmethod
    async def rollback(self):
        ...


class UnitOfWork(IUnitOfWork):
    def __init__(self, repo_class):
        self.session_factory = async_session_maker
        self.repo = repo_class

    async def __aenter__(self):
        self.session = self.session_factory()

        # и еще сюда его добавили
        self.repo = self.repo(self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

def uowfabric(repo_class):
    return UnitOfWork(repo_class)