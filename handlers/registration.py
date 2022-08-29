import logging

from aiogram.dispatcher.filters.state import State, StatesGroup

from herzen import parser
from bot import dp


# states
class UserForm(StatesGroup):
    branch = State()  
    study_form = State()
    group = State()


@dp.message_handler(commands=["register"])
async def start_register(message, state):
    await UserForm.branch.set()
    await message.answer("Введите филиал/факультет из предложенного списка:")

    # saving parsed data to storage
    async with state.proxy() as data:
        data["data"] = parser.get_schedule_data()

        await message.answer("\n".join([f"{i+1}: {branch}" 
            for i, branch in enumerate(data["data"].keys())]))


@dp.message_handler(commands=["cancel"], state=UserForm.all_states)
async def cancel_register(message, state):
    current_state = await state.get_state()
    if current_state is None:
        return
    
    await state.finish()
    await message.answer("Процесс регистрации отменен.")


@dp.message_handler(lambda message: not message.text.isdigit(), state=UserForm.all_states)
async def process_state(message):
    await message.answer("Пожалуйста, введите число, указанное в списке. \
Для выхода из формы регистрации - используйте команду /cancel")


@dp.message_handler(state=UserForm.branch)
async def process_branch(message, state):
    async with state.proxy() as data:
        try:
            branches = list(data["data"].keys())
            chosen_branch = branches[int(message.text) - 1]
            await message.answer(f"Вы выбрали \"{chosen_branch}\"")
            data["branch"] = chosen_branch
        except (IndexError, ValueError):
            await message.answer("Пожалуйста, введите корректный номер для филиала/факультета.")
            return

        branch = data["data"][data["branch"]]
        study_forms = list(branch.keys())
        data["study_forms"] = study_forms
        # if more than 1 study form
        if len(study_forms) > 1:
            await message.answer("Выберите форму обучения:")
            await message.answer("\n".join([f"{i+1}: {branch}" for i, branch in enumerate(study_forms)]))
        else:
            data["study_form"] = study_forms[0]
            groups = list(data["data"][data["branch"]][data["study_form"]])
            data["groups"] = groups
            await message.answer("Выберите группу:")
            await message.answer("\n".join([f"{i+1}: {branch}" for i, branch in enumerate(groups)]))
            await UserForm.next()

    await UserForm.next()


@dp.message_handler(state=UserForm.study_form)
async def process_study_form(message, state):
    async with state.proxy() as data:
        try:
            data["study_form"] = data["study_forms"][int(message.text) - 1]
        except (IndexError, ValueError):
            await message.answer("Пожалуйста, введите корректный номер для формы обучения.")
            return
        groups = list(data["data"][data["branch"]][data["study_form"]])
        data["groups"] = groups
        await message.answer("Выберите группу:")
        await message.answer("\n".join([f"{i+1}: {group}" for i, group in enumerate(groups)]))
    await UserForm.next()


@dp.message_handler(state=UserForm.group)
async def process_group(message, state):
    async with state.proxy() as data:
        try: 
            data["group"] = data["groups"][int(message.text) - 1]
        except (IndexError, ValueError):
            await message.answer("Пожалуйста, введите корректный номер группы.")
            return

        await message.answer(f"{data['branch']}\n{data['study_form']}\n{data['group']}")
    await state.finish()
