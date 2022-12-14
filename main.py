# библиотеки
from ast import parse
from cgitb import text
from fileinput import filename
from time import sleep
from unicodedata import name
from numpy import select
import telebot  # библиотека работы с Telegram API
from telebot import types
import pysondb  # библиотека json базы данных
import datetime
import random

from tomlkit import date  # библиотека времени
# классы
import texts  # texts.py - строки приложения
import markups  # markups.py - кнопки приложения
# ---------------------------------------------
bot = telebot.TeleBot('00000000:XXXXXXXXXXXXXXXXXXXXXXXXX', parse_mode='None')  # Token Insert
users = pysondb.getDb('users.json')
point = [pysondb.getDb('point1.json'), pysondb.getDb('point2.json'), pysondb.getDb('point3.json'), pysondb.getDb('point4.json')]
admins = pysondb.getDb('admins.json')
ban = pysondb.getDb('banned.json')

globalDate = datetime.datetime.today()
nextStepHandler = bot.register_next_step_handler  # переназначение комманды

#Добавление времени к print 
old_print = print
def timestamped_print(*args, **kwargs):
  old_print(datetime.datetime.now(), *args, **kwargs)
print = timestamped_print
# инструменты (в основном работа с атой)
class instruments:
    def checkForwardTime(pointNum, time, date):
        forwardTime = 0
        #print(str(dataBase.points.timeExist(pointNum, time+forwardTime, date)))
        while not dataBase.points.timeExist(pointNum, time+forwardTime, date) and forwardTime <= 5:
            forwardTime+=1
            #print(str(forwardTime))
        return forwardTime
    #установка дат недели
    def weekSet(today):
        weekday = today.weekday()
        i = weekday
        decay = 0
        while(i < 7):
            currentDate = today+datetime.timedelta(days=decay)
            texts.dates[i] = str(currentDate.timetuple()[2]) + '.' + str(currentDate.timetuple()[1])
            i+=1
            decay+=1
        i = 0
        decay = 0
        while(i < weekday):
            currentDate = today+datetime.timedelta(days=7-weekday+decay)
            texts.dates[i] = str(currentDate.timetuple()[2]) + '.' + str(currentDate.timetuple()[1])
            i+=1
            decay+=1
        """#test
        for x in texts.dates:
            print(str(texts.dates.index(x)) + ':' + x)
        """
    #форматирование даты
    def formatDate(data):
        value = ''
        index = data.index('.')
        if index != 2:
            value += '0' + data[:index] + '.'
        else: 
            value += data[:index] + '.' 
        if len(data[index+1:]) < 2:
            value += '0' + data[index+1:]
        else:
            value += data[index+1:]
        return value

    def freeTimeCheck(pointNum, date):
        #print('Date in freeTimeCheck: ' + date) #debugprint
        time1 = 10
        time2 = 24
        freePoint = [False] * 24
        i = time1
        while(i < time2):
            add = 1
            if dataBase.points.timeExist(pointNum, i, date):
                freePoint[i] = False
                add += dataBase.points.timeDuration(pointNum, i, date)
            else:
                freePoint[i] = True
            i+=add 
        return freePoint

    def timeMarkupConstruct(pointNum, date):
        time1 = 10
        time2 = 24
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        freePoint = instruments.freeTimeCheck(pointNum, date)
        i = time1
        markup.add(types.KeyboardButton(texts.buttons.choice.back))
        while(i < time2):
            if freePoint[i] == True:
                markup.add(types.KeyboardButton(str(i) + ':00'))
            i+=1
        return markup
def main():
    print('Bot is staring...')
    global globalDate
    instruments.weekSet(globalDate)
    """#data test
    for x in texts.dates:
        print(instruments.formatDate(x))
    """
main()

# комманда запуска
@bot.message_handler(commands=['start'])
def start(message):
        if message.chat.type == 'private':
            random.seed()
            q = random.choices(texts.quotes, weights=[20, 20, 20, 20, 3, 20, 20, 20, 20, 20], k=1)
            print('/start: ' + str(message.from_user.id))
            bot.send_photo(message.chat.id, open('images/main.png', 'rb'),'Приветствуем в Сообществе Уличных Музыкантов! Если вы хотите послушать уличных музыкантов, нажмите на кнопку "' + texts.buttons.start.button1 + '".\n Если вы сами являетесь исполнителем, то можете забронировать выступление используя кнопку "' + texts.buttons.start.button2 + '". \n\n_' + q[0] + '_', reply_markup=markups.start, parse_mode='Markdown')
    
def admin(message):
    if len(admins.reSearch('tid', message.from_user.id)) > 0:
        bot.send_message(message.chat.id, 'Добро пожаловать в администрационную панель', reply_markup=markups.adminmenu)
        nextStepHandler(message, adminInputParse)
        pass
    else:
        bot.send_message(message.chat.id, 'Access denied')
def adminInputParse(message):
    match message.text:
        case 'Download databases':
            bot.send_document(message.chat.id, open("point1.json","rb"), visible_file_name='point1.json')
            bot.send_document(message.chat.id, open("point2.json","rb"), visible_file_name='point2.json')
            bot.send_document(message.chat.id, open("point3.json","rb"), visible_file_name='point3.json')
            bot.send_document(message.chat.id, open("users.json","rb"), visible_file_name='users.json')
            bot.send_document(message.chat.id, open("banned.json","rb"), visible_file_name='banned.json')
            bot.send_document(message.chat.id, open("admins.json","rb"), visible_file_name='admins.json', caption='Done!')
        case 'Add admin by TID':
            bot.send_message(message.chat.id, 'Write TID:')
            nextStepHandler(message, addTID)
        case 'Unban by TID':
            bot.send_message(message.chat.id, 'Write TID:')
            nextStepHandler(message, unbanTID)
        case 'Remove admin by TID':
            bot.send_message(message.chat.id, 'Write TID:')
            nextStepHandler(message, removeTID)
        case 'Ban by TID':
            bot.send_message(message.chat.id, 'Write TID:')
            nextStepHandler(message, banTID)
        case '/start':
            start(message)
        case 'Upload databases':
            pass
        case 'Change main chat':
            nextStepHandler(message, adminChangeChat)
        case _:
            nextStepHandler(message, adminInputParse)
def adminChangeChat(message):
    chatid = open('chatid', 'w')
    chatid.truncate()
    chatid.write(message.text)
    chatid.close()
    bot.send_message(message.chat.id, 'Done!')

def addTID(message):
    try:
        admins.add({'tid': int(message.text)})
        bot.send_message(message.chat.id, 'done!:' + message.text)
    except Exception:
        pass
    admin(message)
def removeTID(message):
    data = admins.reSearch('tid', message.text)
    if len(data) > 0:
        admins.deleteById(data[0]['id'])
    else: 
        bot.send_message(message.chat.id, 'TID not exist' + message.text)
    bot.send_message(message.chat.id, 'done!:' + message.text)
    admin(message)
def banTID(message):
    try:
        ban.add({'tid': int(message.text)})
        bot.send_message(message.chat.id, 'done!:' + message.text)
    except Exception:
        pass
    admin(message)
def unbanTID(message):
    data = ban.reSearch('tid', message.text)
    if len(data) > 0:
        ban.deleteById(data[0]['id'])
    else: 
        bot.send_message(message.chat.id, 'TID not exist' + message.text)
    bot.send_message(message.chat.id, 'done!:' + message.text)
# класс основного управления
class mainCommands:
    @bot.message_handler(commands=['setmainchat'])
    def mainchat(message):
        if(message.chat.type != 'private'):
            with open('chatid', 'r+') as chatid:
                    chatid.truncate(0)
                    chatid.write(str(message.chat.id))
                    bot.send_message(message.chat.id, 'Теперь этот бот присылает сюда обновления в расписании!')
    # парсер ввода
    @bot.message_handler(content_types=['text'])
    def inputparser(message):
        if(message.chat.type == 'private'):
            match message.text:
                case '/admin':
                    admin(message)
                case texts.buttons.start.button1:  # расписание
                    print('buttons.start.button1(Table): ' + str(message.from_user.id))
                    mainCommands.sendPointsList(message)
                case texts.buttons.start.button2:  # резерв
                    mainCommands.reservePoint(message)
                    print('buttons.start.button2(Reserve): ' + str(message.from_user.id))
                    print('Reserve exist: ' + str(dataBase.points.checkExistingReserve(message.from_user.id)))
                case texts.buttons.start.deleteAccount:  # удаление Аккаунта
                    deleteAccount.delete(message)
                    print('buttons.start.deleteAccount: ' + str(message.from_user.id))
                case texts.buttons.start.about:  # информация о боте
                    print('buttons.start.about: ' + str(message.from_user.id))
                    bot.send_message(message.chat.id, 'Этот бот создан @leracpp.\nОн находится в стадии бета-теста, некоторые функции могут не работать, могут возникать баги и ошибки. По всем вопросам и предложениям, помощи в отладке и исправлении багов писать в личку. *\nПравила пользования:\n-Запрещены названия связаные с экстремизмом или экстремистскими материалами \n(http://mininform.gov.by/documents/respublikanskiy-spisok-ekstremistskikh-materialov/)\n-Запрещёно злоупотребление багами и ошибками(абуз)*\nВерсия: 0.9.3', parse_mode='Markdown');
                case texts.buttons.choice.back:
                    start(message)
    # функция отправки расписания
    def sendPointsList(message):
        for x in point:
            table = ''
            table += '\U0001F4CD' + texts.pointNames[point.index(x)] + '\n\n'
            i=0
            while (i < len(texts.dates)): 
                #print(str(x.getAll())) #debugprint
                currentdate = texts.dates[i]
                #print('date:' + currentdate) #debugprint
                datadate = x.reSearch('date', currentdate)
                if len(datadate) != 0:
                    table += '\U0001F4C5' + texts.weekdaysfull[i] + ' ' + instruments.formatDate(texts.dates[i]) + ':\n'
                    z = 0
                    while (z < 25):
                        for y in datadate:
                            if y['time'] == z:
                                table += '⌛' + texts.messages.list.time + '' + str(y['time']) + ':00-' + str(y['time']+y['duration']) + ':00\n'
                                table += '🎹' + texts.messages.list.bandname + '' + y['bandname'] + '' + '\n'
                                #table += y['description'] + '\n'
                                #table += str(y['duration']) + '\n'
                                #table += y['date'] + '\n'
                                #table += y['number'] + '\n'
                                #table += str(y['tid']) + '\n'
                                table += '📞' + texts.messages.list.login + '@' + str(y['login']) + '\n\n'
                                #table += str(y['id']) + '\n\n'
                        z+=1 
                    #print('datadate:' + str(datadate)) #debugprint
                i+=1
            if table == '\U0001F4CD' + texts.pointNames[point.index(x)] + '\n\n':            
                table += texts.messages.list.listempty 
            """while i < len(x.getAll()):
                table += x.getAll()[i]['bandname'] + '\n'
                table += x.getAll()[i]['description'] + '\n'
                table += str(x.getAll()[i]['time']) + '\n'
                table += str(x.getAll()[i]['duration']) + '\n'
                table += x.getAll()[i]['date'] + '\n'
                table += x.getAll()[i]['number'] + '\n'
                table += str(x.getAll()[i]['tid']) + '\n'
                table += x.getAll()[i]['login'] + '\n'
                table += str(x.getAll()[i]['id']) + '\n\n'
                i+=1"""
            bot.send_message(message.chat.id, table, parse_mode='None')
    # функция резерва
    def reservePoint(message):
        if len(ban.reSearch('tid', message.from_user.id)) == 0:
            #проверка регистрации
            #print(ban.reSearch('tid', message.from_user.id))
            if len(users.reSearch('tid', message.from_user.id)) > 0:
                bot.send_message(message.chat.id, 'Приветствуем ' + str(dataBase.user.getUserName(message.from_user.id)) + '!\nВы выступаете под названием "' + dataBase.user.getBandName(message.from_user.id) + '"\nВыберите точку на которой собираетесь выступать', reply_markup=markups.points)
                nextStepHandler(message, points.selectPoint)
            else:
                bot.send_message(
                    message.chat.id, 'Вы не зарегистрированы! Отправьте нам свой номер телефона используя кнопку ниже', reply_markup=markups.register)
                nextStepHandler(message, registerAccount.register)
        else:
            #print(ban.reSearch('tid', message.from_user.id))
            bot.send_message(message.from_user.id, 'Access denied')
    def changeName(message):
        if len(message.text) < 48:
            if message.text == '/start':
                start(message)
            else:
                bandname = message.text
                id = dataBase.user.getId(message.from_user.id)
                users.updateById(id, {'bandname': bandname})
                bot.send_message(message.chat.id, 'Имя успешно изменено!')
                sleep(1)
                start(message)
        else:
            bot.send_message('Слишком длинное название. Попробуйте ещё раз')
            nextStepHandler(message, mainCommands.changeName)

# класс бронирования точки
class points:
    def selectPoint(message):
        if message.text == texts.pointNames[0]: 
            points.selectDate(message, 0)
        elif message.text == texts.pointNames[1]: 
            points.selectDate(message, 1)
        elif message.text == texts.pointNames[2]:
            points.selectDate(message, 2)
        elif message.text == texts.pointNames[3]:
            points.selectDate(message, 3)
        elif message.text == texts.buttons.other.deleteReserve:
            points.deleteReserve(message)
        elif message.text == texts.buttons.other.changeName:
            """bot.send_message(message.chat.id, '🖥В разработке...')
            sleep(1)
            start(message)"""
            bot.send_message(message.chat.id, 'Введите новое название:\n*Старые брони остануться со старым названием!*', reply_markup=markups.remove, parse_mode='markdown')
            nextStepHandler(message, mainCommands.changeName)
        elif message.text == texts.buttons.choice.back:
                start(message)
    def selectDate(message, pointNum):
        if dataBase.points.checkExistingReserve(message.from_user.id) < 2:
            dataprint = ''
            for x in texts.dates:
                dataprint += '\n' + texts.weekdays[texts.dates.index(x)] + ': ' + instruments.formatDate(x)
            match pointNum:
                case 0|1|2|3 :
                    bot.send_photo(message.chat.id, open('images/point'+ str(pointNum) + '.png', 'rb'), texts.pointNames[pointNum]+ '\nВыберите дату бронирования:\n' + dataprint, parse_mode='Markdown', reply_markup=markups.weekdays)
                    nextStepHandler(message, points.selectTimeStart, pointNum)
                case texts.buttons.choice.back:
                    mainCommands.reservePoint(message)
                case _:
                    bot.send_message(message.chat.id, 'Команда не распознана', reply_markup=markups.points)
                    nextStepHandler(message, points.selectPoint)
        else:
            bot.send_message(message.chat.id, 'У вас уже есть активные брони (Максимум 2 по 6 часов). Удалите предыдущие брони или дождитесь окончания вашего выступления')
            sleep(1)
            start(message)
    def selectTimeStart(message, pointNum):
        weekday = None
        for x in texts.weekdays:
            if message.text == x:
                weekday = texts.weekdays.index(x)
        if weekday is not None:
            #print('points.selectTimeStart:' + str(message.from_user.id) + '\n {weekday, texts.dates[weekday]}\n{' + str(weekday) + ', ' + str(texts.dates[weekday]) + '}')
            bot.send_message(message.chat.id, 'Дата: ' + instruments.formatDate(texts.dates[weekday]) + '\nТочка: ' + texts.pointNames[pointNum] + '\nУкажите время начала:', reply_markup=instruments.timeMarkupConstruct(pointNum, texts.dates[weekday]))
            nextStepHandler(message, points.selectDuration, pointNum, texts.dates[weekday])
        elif message.text == texts.buttons.choice.back:
            mainCommands.reservePoint(message)
        else:
            bot.send_message('Некорректная дата')
            nextStepHandler(message, points.selectTimeStart, pointNum)
    def selectDuration(message, pointNum, date):
        freepoint = instruments.freeTimeCheck(pointNum, date)
        if ":00" in message.text:
            if len(message.text) > 4:
                time = int(message.text[:2])
            else:
                time = int(message.text[:1])
            if time > 24 or time < 10:
                bot.send_message(message.chat.id, 'Некорректное время')
                nextStepHandler(message, points.selectDuration, pointNum, date)
            elif freepoint[time] == False:
                bot.send_message(message.chat.id, 'Это время недоступно')
                nextStepHandler(message, points.selectDuration, pointNum, date)
            else: 
                bot.send_message(message.chat.id, 'Выберите продолжительность выступления', reply_markup=markups.duration)
                nextStepHandler(message, points.confirmReserve, pointNum, date, time)
                #print(str(pointNum) + ', ' + date + ', ' + str(time) + ':00, ' + str(message.from_user.id))
        elif message.text == texts.buttons.choice.back:
            points.selectTimeStart(message, pointNum)
    def confirmReserve(message, pointNum, date, time):
        try:
            if int(message.text[:1]) <= instruments.checkForwardTime(pointNum, time, date) and not (int(message.text[:1]) > 1 and time == 23) and not (int(message.text[:1]) > 2 and time == 22) and not (int(message.text[:1]) > 3 and time == 21) and not (int(message.text[:1]) > 4 and time == 20) and not (int(message.text[:1]) > 5 and time == 19) and not (int(message.text[:1]) > 6 and time == 18):
                duration = int(message.text[:1])
                bot.send_message(message.chat.id, 'Проверьте правильность введённых данных:\nИсполнитель: ' + dataBase.user.getBandName(message.from_user.id) + '\nДата: ' + instruments.formatDate(date) + '\nВремя: ' + str(time) + ':00\nПродолжительность выступления: ' + str(duration) + ' часов (до ' + str(time + duration) +':00 часов)', reply_markup=markups.confirm)
                nextStepHandler(message, points.saveReserve, pointNum, date, time, duration)
            else: raise Exception()
        except:
            bot.send_message(message.chat.id, 'Не верная продолжительность (Максимум 6 часов) или ваша бронь пересекается с последующей', reply_markup=markups.duration)
            nextStepHandler(message, points.confirmReserve, pointNum, date, time)          
    def saveReserve(message, pointNum, date, time, duration):
        if message.text == texts.buttons.choice.correct:
            tid = message.from_user.id
            reserve = dataBase.points.addReserve(pointNum, dataBase.user.getBandName(tid),'', time, duration, date, dataBase.user.getNumber(tid), tid, str(dataBase.user.getUserName(tid)))
            print('Reserved:' + str(point[pointNum].getById(reserve)))
            bot.send_message(message.chat.id, 'Успешно зарезервировано!')
            start(message)
        else:
            bot.send_message(message.chat.id, 'Резерв отменён')
            mainCommands.reservePoint(message)
            pass
    def deleteReserve(message):
        bot.send_message(message.chat.id, 'Вы уверены что хотите удалить все брони? Их придётся регистрировать заново. \n*Будут удалены резервы только вашего аккаунта!*', reply_markup=markups.choice, parse_mode='Markdown')
        nextStepHandler(message, points.confirmRemoveReserve)
    def confirmRemoveReserve(message):
        if message.text == texts.buttons.choice.yes:
            dataBase.points.removeReserveFromDB(message)
            bot.send_message(message.chat.id, 'Все брони удалены!')
            print('Reserves deleted: ' + str(message.from_user.id))
            sleep(1)
            start(message)
        else:
            bot.send_message(message.chat.id, 'Отменено')
            sleep(1)
            start(message)
# класс удаления аккаунта
class deleteAccount:
    def delete(message):
        if len(users.reSearch('tid', message.from_user.id)) > 0:
            bot.send_message(message.chat.id, 'Вы действительно хотите удалить аккаунт? *Все брони будут автоматически удалены!*', reply_markup=markups.choice, parse_mode='Markdown')
            nextStepHandler(message, deleteAccount.confirm)
        else:
            bot.send_message(message.chat.id, 'Аккаунта не существует')
            sleep(1)
            start(message)
    def confirm(message):
        if message.text == texts.buttons.choice.yes:
            id = users.reSearch('tid', message.from_user.id)[0]['id']
            dataBase.points.removeReserveFromDB(message)
            users.deleteById(id)
            bot.send_message(message.chat.id, 'Аккаунт удалён', reply_markup=markups.remove)
            sleep(1)
            start(message)
        else:
            bot.send_message(message.chat.id, 'Отменено', reply_markup=markups.start)
            sleep(1)
            start(message)
# класс регистрации аккаунта
class registerAccount:
    # начало регистрации
    def register(message):
        # проверка корректного номера
        if message.contact is not None:
            number = message.contact.phone_number
            login = message.from_user.username
            bot.send_message(message.chat.id, 'Хорошо! Теперь введите название коллектива(исполнителя). Подумайте хорошо. В дальнейшем поменять его будет невозможно!\nПравила оформления:\n*-Название не должно быть больше 24 символов*\n-Каждое слово должно быть с заглавной буквы(Или же полностью состоять из заглавных букв)', reply_markup=markups.remove, parse_mode='Markdown')
            nextStepHandler(message, registerAccount.step2, number, login)
        elif message.text == '/start':
            start(message)
        else:
            bot.send_message(message.chat.id, texts.errors.register.phoneError)

    def step2(message, number, login):
        if len(message.text) < 48:
            bandname = message.text
            users.add({'bandname': bandname, 'tid': message.from_user.id,
                       'number': number, 'login': login})
            bot.send_message(message.chat.id, 'Вы успешно зарегистрированы!')
            print('Registered: ' + str(users.reSearch('tid', message.from_user.id)))
            sleep(1)
            start(message)
        else:
            bot.send_message(
                message.chat.id, 'Слишком длинное название. Попробуйте ещё раз.')
            nextStepHandler(message, registerAccount.step2, number, login)
# управление базой данных
class dataBase:
    class user:
        def getParam(tid, param):
            try:
                out = users.reSearch('tid', tid)[0][param]
            except:
                return None
            return out
        def getBandName(tid):
            try:
                out = users.reSearch('tid', tid)[0]['bandname']
            except:
                return None
            return out
        def getUserName(tid):
            try:
                out = users.reSearch('tid', tid)[0]['login']
            except:
                return None
            return out
        def getNumber(tid):
            try:
                out = users.reSearch('tid', tid)[0]['number']
            except:
                return None
            return out
        def getId(tid):
            try:
                out = users.reSearch('tid', tid)[0]['id']
            except:
                return None
            return out    
        
    class points:
        def checkExistingReserve(tid):
            result = 0
            for x in point:
                i = 0
                data = x.getAll()
                while(i < len(texts.dates)):
                    o = 0
                    while(o < len(data)):
                        if data[o]['date'] == texts.dates[i]:
                            if data[o]['tid'] == tid:
                                result += 1
                        o += 1
                    i += 1
            return result
        def removeReserveFromDB(message):
            for x in point:
                i = 0
                data = x.getAll()
                while(i < len(data)):
                    if data[i]['tid'] == message.from_user.id:
                        id = data[i]['id']
                        point[point.index(x)].deleteById(id)
                    i+=1
        def addReserve(pointNum, bandname, description, time, duration, date, number, tid, login):
            ret = point[pointNum].add({'bandname': bandname, 'description': description, 'time': time, 'duration': duration, 'date': date, 'number': number, 'tid': tid, 'login': login})
            with open('chatid', 'rb') as chatid:
                index = date.index('.')
                operationalDate = datetime.datetime(globalDate.year, int(date[index+1:]), int(date[:index]))
                weekday = operationalDate.weekday()
                try:
                    bot.send_message(int(chatid.readline()), 'Новая бронь!\n\n📍' + texts.pointNames[pointNum] + '\n\n📅' + texts.weekdaysfull[weekday]+ ' ' + instruments.formatDate(date) + ':\n⌛️Время выступления: ' + str(time) + ':00-' + str(time+duration) + ':00\n🎹Название исполнителя: ' + bandname + '\n📞Контактные данные выступающего: @' + login, reply_markup=markups.remove)
                except Exception:
                    pass
            return ret
        def timeExist(pointNum, time, date):
            try:
                dates = point[pointNum].reSearch('time', time)
                #print('input date:' + date) #debugprint
                for x in dates:
                    #print('output date: ' + x['date'])
                    if x['date'] == date:
                        return True
                else:
                    return False
            except:
                return False
        def timeDuration(pointNum, time, date):
            try:
                duration = point[pointNum].reSearch('date', date)
                for x in duration:
                    if x['time'] == time:
                        return x['duration']
                    else:
                        return 0
            except:
                return None



#####
bot.infinity_polling(10000)  # Init infinity cycle timeout=10000
