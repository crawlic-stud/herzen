import logging
from venv import create

from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.exceptions import Throttled

from herzen import parser
from config import dp, database, bot
from database import User, UserData
from messages import CANCEL_REGISTRATION_MESSAGE
from keyboards import REGISTER_KEYBOARD, AFTER_REGISTRATION_KEYBOARD
from utils import create_inline_list, create_inline_table
from handlers.spam_handler import on_spam


# states
class UserForm(StatesGroup):
    branch = State()  
    study_form = State()
    group = State()



@dp.message_handler(commands=["register"])
@dp.throttled(on_spam, rate=3)
async def start_register(message, state):
    await UserForm.branch.set()

    # saving parsed data to memory storage
    async with state.proxy() as data:
        data["data"] = parser.get_schedule_data()
        data["branches"] = list(data["data"].keys())
        if "Bad response" in data["branches"]:
            await message.answer(f"⚠️ Ошибка. Возможно, что-то не так с <a href='{parser.SCHEDULE_URL}'>сайтом</a>.")
        await message.answer("<b>Регистрация.</b>\nВыберите филиал/факультет из предложенного списка:", 
            reply_markup=create_inline_list(data["branches"]))


async def show_user_data(message, user_id, user_full_name):
    user_data = database.get_user_data(user_id)
        
    message_text = "Пользователь не найден. Возможно, Вы еще не зарегистрировались?"
    if user_data:
        message_text = f"<b>Текущие данные для {user_full_name}:</b>\n - {user_data.branch}\n\
 - {user_data.study_form}\n - {user_data.group}"

    await message.answer(message_text, reply_markup=REGISTER_KEYBOARD)


@dp.message_handler(commands=["me"])
@dp.throttled(on_spam, rate=3)
async def show_my_data(message, state):
    user_data = database.get_user_data(message.from_id)

    message_text = "Пользователь не найден. Возможно, Вы еще не зарегистрировались?"
    if user_data:
        message_text = f"<b>Текущие данные для {message.from_user.full_name}:</b>\n - {user_data.branch}\n\
 - {user_data.study_form}\n - {user_data.group}"

    await message.answer(message_text, reply_markup=REGISTER_KEYBOARD)

@dp.message_handler(commands=["cancel"], state=UserForm.all_states)
async def cancel_register(message, state):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.finish()
    await message.answer("Процесс регистрации отменен.")


@dp.callback_query_handler(lambda query: query.data.isdigit(), state=UserForm.branch)
async def process_branch_state(query, state):
    async with state.proxy() as data:
        data["branch"] = data['branches'][int(query.data)]
        data["study_forms"] = list(data["data"][data["branch"]].keys())

        await bot.answer_callback_query(query.id, f"Выбрано {data['branch']}")
        if (len(data["study_forms"]) > 1):
            await query.message.edit_text("Выберите форму обучения:", reply_markup=create_inline_list(data["study_forms"]))
            await UserForm.study_form.set()
        else:
            data["study_form"] = data["study_forms"][0]
            data["groups"] = list(data["data"][data["branch"]][data["study_form"]].keys())
            await query.message.edit_text("Выберите группу:", reply_markup=create_inline_table(data["groups"]))
            await UserForm.group.set()


@dp.callback_query_handler(lambda query: query.data.isdigit(), state=UserForm.study_form)
async def process_study_form_state(query, state):
    async with state.proxy() as data:
        data["study_form"] = data["study_forms"][int(query.data)]

        await bot.answer_callback_query(query.id, f"Выбрано {data['study_form']}")
        data["groups"] = list(data["data"][data["branch"]][data["study_form"]].keys())
        await query.message.edit_text("Выберите группу:", reply_markup=create_inline_table(data["groups"]))
        await UserForm.group.set()


@dp.callback_query_handler(lambda query: query.data.isdigit(), state=UserForm.group)
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
        success = database.set_user(user)
        if success:
            await query.message.edit_text(f"<b>Регистрация завершена, записанные данные:</b>\
\n - {user.data.branch}\n - {user.data.study_form}\n - {user.data.group}", 
                reply_markup=AFTER_REGISTRATION_KEYBOARD)
        else:
            await query.message.edit_text("<b>Что-то пошло не так. Попробуйте снова :(</b>", reply_markup=None)
        await state.finish()


@dp.message_handler(state=UserForm.all_states)
async def process_wrong_input(message):
    await message.answer(CANCEL_REGISTRATION_MESSAGE)
