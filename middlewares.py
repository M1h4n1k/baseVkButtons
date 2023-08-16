from vkbottle import BaseMiddleware, CtxStorage
from vkbottle.bot import Bot, Message
from models import async_session, User


class RegistrationMiddleware(BaseMiddleware[Message]):
    session = None

    async def pre(self):
        async with async_session() as session:
            self.session = session
            self.send({"session": session})

    async def post(self):
        if self.session is not None:
            await self.session.close()
