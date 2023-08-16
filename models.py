from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text, Boolean, func, BIGINT
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_async_engine("sqlite+aiosqlite:///./db.sqlite3")
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    vk_id = Column(BIGINT, unique=True, primary_key=True)
    join_date = Column(DateTime(timezone=True), default=func.now())
    first_name = Column(Text, default='')
    last_name = Column(Text, default='')
    age = Column(Integer, default=0)
    gender = Column(Integer, default=0)

    def __repr__(self):
        return f"User(vk_id={self.vk_id!r}, " \
               f"join_date={self.join_date!r}, " \
               f"first_name={self.first_name!r}, " \
               f"last_name={self.last_name!r}, " \
               f"age={self.age!r}," \
               f"gender={self.gender!r})"
