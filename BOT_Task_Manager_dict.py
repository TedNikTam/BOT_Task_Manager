'''Регистрация и редактирование задачи в словаре'''
import telebot

bot = telebot.TeleBot('7016733305:AAES3DPE1D0QuUbzkQtkXz8IazclmxwqymU')
task_descrip = None
task_descrip_dict = {}
task_name = None

# =================СОЗДАНИЕ ЗАДАЧ==================
@bot.message_handler(commands=['add'])
def start(message):
    # описания задачи
    bot.send_message(message.chat.id, 'Введите описание задачи.')
    bot.register_next_step_handler(message, task_description)

def task_description(message):
    # запрос статуса задачи
    global task_descrip
    task_descrip = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите статус задачи.')
    bot.register_next_step_handler(message, task_status)
    
def task_status(message):
    # окончание регистрации задачи
    password = message.text.strip()
    task_descrip_dict[task_descrip] = password
    
    bot.send_message(message.chat.id, 'Задача зарегистрирована.\nМожно проверить с помощью команды "/list"')
    # for key, value in task_descrip_dict.items():
    #     print(f'{key}: {task_descrip_dict[key]}')

# =================ПРОСМОТР СПИСКА И СТАТУСА ЗАДАЧ==================
@bot.message_handler(commands=['list'])
def show_list(message):
    # создается ответ по команде
    global task_descrip_dict
    for task, status in task_descrip_dict.items():
        bot.send_message(message.chat.id, f'{task}: {status}')

# =================ИЗМЕНЕНИЕ СТАТУСА ЗАДАЧ==================
@bot.message_handler(commands=['done'])
def start_edit_dict(message):
    # создается запрос на изменение статуса задачи по запросу её названия
    bot.send_message(message.chat.id, 'Введите название задачи')
    bot.register_next_step_handler(message, edit_dict)

def edit_dict(message):
    # запоминается название задачи и запрашивается её новый статус
    global task_name
    task_name = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите новый статус')
    bot.register_next_step_handler(message, new_status)

def new_status(message):
    # записывается НОВЫЙ статус задачи
    new_status = message.text.strip()
    task_descrip_dict[f'{task_name}'] = new_status
    bot.send_message(message.chat.id, f'Изменения вступили в силу.\nМожно проверить с помощью команды "/list"')

bot.polling(non_stop=True)