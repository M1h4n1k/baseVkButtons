from datetime import date
from config import api
from models import User


def calculate_age(dob):
    today = date.today()
    return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))


async def create_user(event, session):
    await api.users.get(event.from_id)
    vk_user = await api.users.get(event.from_id, fields=['bdate', 'sex'])
    vk_user = vk_user[0]
    if vk_user.bdate is None or len(vk_user.bdate.split('.')) != 3:
        bdate = None
    else:
        bdate = vk_user.bdate.split('.')
        bdate = date(int(bdate[2]), int(bdate[1]), int(bdate[0]))
    user = User(
        vk_id=event.from_id,
        first_name=vk_user.first_name,
        last_name=vk_user.last_name,
        age=calculate_age(bdate) if bdate is not None else -1,
        sex=vk_user.sex
    )
    session.add(user)
    await session.commit()
    await session.flush()
    return user