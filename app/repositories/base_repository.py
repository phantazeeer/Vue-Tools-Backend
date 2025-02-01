from abc import ABC, abstractmethod

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def find_one(self):
        raise NotImplementedError

    @abstractmethod
    async def del_one(self):
        raise NotImplementedError


class Repository(AbstractRepository):
    model = None
    # стандартный CRUD весь лежит здесь

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict):
        # добавление одного экземпляра для любой модели
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def find_all(self):
        # поиск всех экземпляров для любой модели
        res = await self.session.execute(select(self.model))
        # в res лежитт объект sqlalchemy типа:
        # <sqlalchemy.engine.result.ChunkedIteratorResult object at 0x00000176F6EB9500>
        # этот объект нужно разбить на список результирующих строк (объектов модели бд)
        # следующий метод работает по аналогии с fetchall()
        return res.scalars().all()

    async def find_one(self, **filter_by):
        # поиск одного экземпляра для любой модели
        # в аргументах получаем словарь, по которому производится поиск нужного элемента
        res = await self.session.execute(select(self.model).filter_by(**filter_by))
        res = res.scalar_one()
        return res

    async def del_one(self, **filter_by):
        # удаление одного экземпляра из любой модели по id
        stmt = delete(self.model).where(self.model.id == filter_by['id']).returning(self.model)
        res = await self.session.execute(stmt)
        res = res.scalar_one()
        return res