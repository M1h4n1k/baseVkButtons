from vkbottle.bot import BotLabeler
from vkbottle import BaseStateGroup
from config import state_dispenser
from models import User
from vkbottle import Keyboard, KeyboardButtonColor, Text
from .misc_handlers import default_handler


class AgeStates(BaseStateGroup):
    SET_AGE = 'set_age'


age_labeler = BotLabeler()


@age_labeler.message(payload={'cmd': 'age'})
async def age_handler(event, session) -> dict:
    user = await session.get(User, event.from_id)
    await state_dispenser.set(event.from_id, AgeStates.SET_AGE)
    keyboard = Keyboard(inline=True)
    if user.age != -1:
        keyboard.add(Text(str(user.age)), color=KeyboardButtonColor.POSITIVE)
    keyboard.add(Text('Назад', payload={'cmd': 'cancel'}), color=KeyboardButtonColor.NEGATIVE)

    return {
        'message': 'Сколько тебе лет?',
        'keyboard': keyboard.get_json()
    }


@age_labeler.message(state=AgeStates.SET_AGE)
async def set_age(message, session) -> dict:
    if not message.text.isdigit():
        return {
            'message': 'Возраст должен быть числом'
        }
    age = int(message.text)
    if age < 14 or age > 90:
        return {
            'message': 'Возраст должен быть в диапазоне от 14 до 90'
        }
    user = await session.get(User, message.from_id)
    user.age = age
    await session.commit()
    await state_dispenser.delete(message.from_id)
    return await default_handler(message, session)


