import logging
from venv import create

from aiogram.dispatcher.filters.state import State, StatesGroup

from herzen import parser
from config import dp, database, bot
from herzen.get_schedule import get_date_schedule_link, get_full_schedule_link, get_table_from_link, get_today_link
from database import User, UserData
from messages import CANCEL_REGISTRATION_MESSAGE
from utils import create_inline_keyboard


# states
class UserForm(StatesGroup):
    branch = State()  
    study_form = State()
    group = State()


@dp.callback_query_handler(state=UserForm.branch)
async def process_branch_state(query, state):
    async with state.proxy() as data:
        data["branch"] = data['branches'][int(query.data)]
        data["study_forms"] = list(data["data"][data["branch"]].keys())

        await bot.answer_callback_query(query.id, f"Выбрано {data['branch']}")
        if (len(data["study_forms"]) > 1):
            await query.message.edit_text("Выберите форму обучения:", reply_markup=create_inline_keyboard(data["study_forms"]))
            await UserForm.study_form.set()
        else:
            data["study_form"] = data["study_forms"][0]
            data["groups"] = list(data["data"][data["branch"]][data["study_form"]].keys())
            await query.message.edit_text("Выберите группу:", reply_markup=create_inline_keyboard(data["groups"]))
            await UserForm.group.set()


@dp.callback_query_handler(state=UserForm.study_form)
async def process_study_form_state(query, state):
    async with state.proxy() as data:
        data["study_form"] = data["study_forms"][int(query.data)]

        await bot.answer_callback_query(query.id, f"Выбрано {data['study_form']}")
        data["groups"] = list(data["data"][data["branch"]][data["study_form"]].keys())
        await query.message.edit_text("Выберите группу:", reply_markup=create_inline_keyboard(data["groups"]))
        await UserForm.group.set()


@dp.callback_query_handler(state=UserForm.group)
async def process_group_state(query, state):
    async with state.proxy() as data:
        data["group"] = data["groups"][int(query.data)]

        await bot.answer_callback_query(query.id, f"Выбрано {data['group']}")

        user = User(
            user_id=query.from_user.id,
            data=UserData(
                branch=data["branch"],
                study_form=data["study_form"],
                group=data["group"]
            )
        )
        database.set_user(user)

        await query.message.edit_text(f"<b>Регистрация завершена, записанные данные:</b>\
\n - {user.data.branch}\n - {user.data.study_form}\n - {user.data.group}", 
            reply_markup=None)
        await state.finish()


@dp.message_handler(commands=["register"])
async def start_register(message, state):
    user_data = database.get_user_data(message.from_id)
    if user_data:
        await message.answer(f"<b>Пользователь уже зарегистрирован, текущие данные:</b>\n - {user_data.branch}\n\
 - {user_data.study_form}\n - {user_data.group}\n\n{CANCEL_REGISTRATION_MESSAGE}")

    await UserForm.branch.set()

    # saving parsed data to memory storage
    async with state.proxy() as data:
        data["data"] = parser.get_schedule_data()
        data["branches"] = list(data["data"].keys())
        await message.answer("Выберите филиал/факультет из предложенного списка:", 
            reply_markup=create_inline_keyboard(data["branches"]))
    

@dp.message_handler(commands=["cancel"], state=UserForm.all_states)
async def cancel_register(message, state):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.finish()
    await message.answer("Процесс регистрации отменен.")


@dp.message_handler(state=UserForm.all_states)
async def process_wrong_input(message):
    await message.answer(CANCEL_REGISTRATION_MESSAGE)
