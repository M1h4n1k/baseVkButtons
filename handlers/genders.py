from vkbottle import Keyboard, KeyboardButtonColor, Text
from models import User
from vkbottle.bot import Message, BotLabeler
from vkbottle.dispatch.rules import ABCRule
from .misc_handlers import default_handler


gender_labeler = BotLabeler()


class GenderRule(ABCRule[Message]):
    def __init__(self, possible_genders: tuple = (0, 1, 2)):
        self.pg = possible_genders

    async def check(self, event: Message) -> bool:
        if event.payload is None:
            return False
        return event.get_payload_json().get('gender', -1) in self.pg


@gender_labeler.message(payload={'cmd': 'gender'})
async def gender_handler(event, session) -> dict:
    user = await session.get(User, event.from_id)
    keyboard = (
        Keyboard(inline=True)
        .add(Text('Мужской', payload={'gender': 0}), color=KeyboardButtonColor.POSITIVE if user.gender == 0 else None)
        .add(Text('Женский', payload={'gender': 1}), color=KeyboardButtonColor.POSITIVE if user.gender == 1 else None)
        .add(Text('Вертолет', payload={'gender': 2}), color=KeyboardButtonColor.POSITIVE if user.gender == 2 else None)
    ).get_json()
    return {
        'message': 'Выберите гендер',
        'keyboard': keyboard
    }


@gender_labeler.message(GenderRule((0, 1, 2)))
async def set_gender(message: Message, session) -> dict:
    gender = int(message.get_payload_json()['gender'])
    user = await session.get(User, message.from_id)
    user.gender = gender
    # probably change the keyboard of the previous message
    await session.commit()
    return await default_handler(message, session)