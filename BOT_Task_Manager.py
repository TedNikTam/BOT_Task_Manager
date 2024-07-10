'''BOT_Task_Manager Работа с задачаими через базу данных sqlite3. Создание, отслеживание и редактирование статуса задач.'''

import telebot
import sqlite3

bot = telebot.TeleBot('7016733305:AAES3DPE1D0QuUbzkQtkXz8IazclmxwqymU')
description = None
task_num = None


# =================СОЗДАНИЕ ЗАДАЧ==================
@bot.message_handler(commands=['add'])
def start(message):
    # создается таблица в базе и запрашивается отписание задачи
    conn = sqlite3.Connection('data.sqlite3')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY AUTOINCREMENT, description varchar(1000), status varchar(10))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Введите описание задачи.')
    bot.register_next_step_handler(message, task_descrip)

def task_descrip(message):
    # записывается описание задачи и запрашивается её стаус
    global description
    description = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите статус')
    bot.register_next_step_handler(message, task_status)

def task_status(message):
    # записывается статус задачи
    status = message.text.strip()

    conn = sqlite3.Connection('data.sqlite3')
    cur = conn.cursor()

    cur.execute("INSERT INTO tasks (description, status) VALUES ('%s', '%s')" % (description, status))
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, f'Задача зарегистрирована!\nМожно проверить с помощью команды "/list"')

    # создается кнопка просмотра данных
    # markup = telebot.types.InlineKeyboardMarkup()
    # markup.add(telebot.types.InlineKeyboardButton('Список задач и статус', callback_data='tasks'))

    # bot.send_message(message.chat.id, 'Задача зарегистрирована!', reply_markup=markup)
    
# =================ПРОСМОТР СПИСКА И СТАТУСА ЗАДАЧ==================
@bot.message_handler(commands=['list'])
def show_list(message):
    # создается ответ по команде
    conn = sqlite3.Connection('data.sqlite3')
    cur = conn.cursor()

    cur.execute("SELECT * FROM tasks")
    tasks = cur.fetchall()

    info = ''
    for el in tasks:
        info += f'Номер: {el[0]}\nОписание: {el[1]}\nСтатус: {el[2]}\n --- --- ---\nИзменить статус задачи можчно с помощью команты "/done"'
        
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, info)

# =================ИЗМЕНЕНИЕ СТАТУСА ЗАДАЧ==================
@bot.message_handler(commands=['done'])
def statrt_edit_list(message):
    # создается запрос на изменение статуса задачи
    
    bot.send_message(message.chat.id, 'Введите номер задачи')
    bot.register_next_step_handler(message, edit_list)

def edit_list(message):
    # запоминается номер задачи
    global task_num
    task_num = message.text.strip()
    bot.send_message(message.chat.id, 'Укажите новый статус')
    bot.register_next_step_handler(message, new_status)

def new_status(message):
    # записывается НОВЫЙ статус задачи
    new_status = message.text.strip()

    conn = sqlite3.Connection('data.sqlite3')
    cur = conn.cursor()

    cur.execute('UPDATE tasks SET status == ? WHERE id == ?', (f'{new_status}', f'{task_num}'))
      
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Изменения вступили в силу.\nМожно проверить с помощью команды "/list"')
    
bot.polling(non_stop=True)