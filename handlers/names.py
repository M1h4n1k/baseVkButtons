from vkbottle.bot import BotLabeler, Message
from vkbottle import Keyboard, KeyboardButtonColor, Text
from vkbottle import BaseStateGroup
from models import User
from config import state_dispenser
from .misc_handlers import default_handler

names_labeler = BotLabeler()


class NamesStates(BaseStateGroup):
    SET_FIRST_NAME = 'fname'
    SET_LAST_NAME = 'lname'


@names_labeler.message(payload={'cmd': 'first_name'})
async def first_name_handler(event, session) -> dict:
    user = await session.get(User, event.from_id)
    await state_dispenser.set(event.from_id, NamesStates.SET_FIRST_NAME)

    keyboard = (
        Keyboard(inline=True)
        .add(Text(str(user.first_name)), color=KeyboardButtonColor.POSITIVE)
        .add(Text('Назад', payload={'cmd': 'cancel'}), color=KeyboardButtonColor.NEGATIVE)
    ).get_json()
    return {
        'message': 'Какое у тебя имя?',
        'keyboard': keyboard
    }


# maybe some validation is needed
@names_labeler.message(state=NamesStates.SET_FIRST_NAME)
async def set_first_name(event, session) -> dict:
    user = await session.get(User, event.from_id)
    user.first_name = event.text
    await session.commit()
    await state_dispenser.delete(event.from_id)
    return await default_handler(event, session)


@names_labeler.message(payload={'cmd': 'last_name'})
async def last_name_handler(event, session) -> dict:
    user = await session.get(User, event.from_id)
    await state_dispenser.set(event.from_id, NamesStates.SET_LAST_NAME)

    keyboard = (
        Keyboard(inline=True)
        .add(Text(str(user.last_name)), color=KeyboardButtonColor.POSITIVE)
        .add(Text('Назад', payload={'cmd': 'cancel'}), color=KeyboardButtonColor.NEGATIVE)
    ).get_json()
    return {
        'message': 'Какая у тебя фамилия?',
        'keyboard': keyboard
    }


# maybe some validation is needed
@names_labeler.message(state=NamesStates.SET_LAST_NAME)
async def set_last_name(event: Message, session) -> dict:
    user = await session.get(User, event.from_id)
    user.last_name = event.text
    await session.commit()
    await state_dispenser.delete(event.from_id)
    return await default_handler(event, session)
