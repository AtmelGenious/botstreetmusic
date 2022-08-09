from numpy import empty
from telebot import types
import texts
    
empty = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)

start = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
start.add(types.KeyboardButton(texts.buttons.start.button1))
start.add(types.KeyboardButton(texts.buttons.start.button2))
start.add(types.KeyboardButton(texts.buttons.start.deleteAccount),types.KeyboardButton(texts.buttons.start.about))

register = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
register.add(types.KeyboardButton(texts.buttons.register.sendPhoneButton, request_contact=True))

remove = types.ReplyKeyboardRemove()

choice = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
choice.add(types.KeyboardButton(texts.buttons.choice.yes), types.KeyboardButton(texts.buttons.choice.no))

points = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
for x in texts.pointNames:
    points.add(types.KeyboardButton(x))
points.add(types.KeyboardButton(texts.buttons.other.deleteReserve), types.KeyboardButton(texts.buttons.other.changeName))
points.add(types.KeyboardButton(texts.buttons.choice.back))

weekdays = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=7)
weekdays.add(types.KeyboardButton(texts.weekdays[0]),types.KeyboardButton(texts.weekdays[1]),types.KeyboardButton(texts.weekdays[2]),types.KeyboardButton(texts.weekdays[3]),types.KeyboardButton(texts.weekdays[4]),types.KeyboardButton(texts.weekdays[5]),types.KeyboardButton(texts.weekdays[6]))
weekdays.add(types.KeyboardButton(texts.buttons.choice.back))

duration = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
duration.add(types.KeyboardButton('1 час'), types.KeyboardButton('2 часа'), types.KeyboardButton('3 часа'))
duration.add(types.KeyboardButton('4 часа'), types.KeyboardButton('5 часов'), types.KeyboardButton('6 часов'))

confirm = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True)
confirm.add(types.KeyboardButton(texts.buttons.choice.correct), types.KeyboardButton(texts.buttons.choice.cancel))

adminmenu = types.ReplyKeyboardMarkup(one_time_keyboard=False, resize_keyboard=True, row_width=1)
adminmenu.add(types.KeyboardButton('Download databases'),types.KeyboardButton('Ban by TID'), types.KeyboardButton('Unban by TID'), types.KeyboardButton('Add admin by TID'), types.KeyboardButton('Remove admin by TID'))