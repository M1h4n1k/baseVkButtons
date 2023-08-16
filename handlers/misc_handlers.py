from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from models import User
from config import state_dispenser, labeler
from .utils import create_user

misc_labeler = BotLabeler()


@labeler.message(payload={'cmd': 'cancel'})
async def cancel_handler(event, session) -> dict:
    await state_dispenser.delete(event.from_id)
    return await default_handler(event, session)


@misc_labeler.message()
async def default_handler(event, session) -> dict:
    # await bot.state_dispenser.delete(event.from_id)
    if await state_dispenser.get(event.from_id) is not None:
        await state_dispenser.delete(event.from_id)
    user = await session.get(User, event.from_id)
    if user is None:
        user = await create_user(event, session)
    keyboard = (
        Keyboard(inline=False, one_time=False)
        .add(Text('Поменять гендер', payload={'cmd': 'gender'}), color=KeyboardButtonColor.POSITIVE)
        .row()
        .add(Text('Поменять имя', payload={'cmd': 'first_name'}))
        .add(Text('Поменять фамилию', payload={'cmd': 'last_name'}))
        .add(Text('Поменять возраст', payload={'cmd': 'age'}))
    ).get_json()
    message = f'Привет, {user.first_name} {user.last_name}!\n'
    if user.age != -1:
        message += f'Тебе {user.age} лет\n'
    message += f'Ты - {["мужчина", "женщина", "вертолет"][user.gender]}'
    return {
        'message': message,
        'keyboard': keyboard
    }

