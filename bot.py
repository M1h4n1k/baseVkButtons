from vkbottle.bot import Bot
from loguru import logger
import sys
from middlewares import RegistrationMiddleware
from models import engine, Base, User
from config import TOKEN, labeler, state_dispenser, api
from handlers import labelers

logger.remove()
logger.add(sys.stdout, level="INFO")

for label in labelers:
    labeler.load(label)
bot = Bot(TOKEN, labeler=labeler, state_dispenser=state_dispenser, api=api)


async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


bot.labeler.message_view.register_middleware(RegistrationMiddleware)
bot.loop_wrapper.add_task(on_startup())
bot.run_forever()

