from webbrowser import get


pointNames = ['0', '1', '2']
weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
weekdaysfull = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
dates = [''] * 7

class buttons:
    class other:
        deleteReserve = 'Удалить бронирование'
        changeName = 'Сменить название'
    class choice:
        yes = '✅Да✅'
        no = '❌Нет❌'
        cancel = '❌Отменить❌'
        back = '🔙 Назад'
        correct = '✅Всё верно✅'
    class start:
        button1 = '📅Расписание выступлений'
        button2 = '🗺Занять точку'
        about = 'ℹО боте'
        deleteAccount = '❌Удалить аккаунт'
    class register:
        sendPhoneButton = 'Отправить номер'
class errors:
    class register:
        phoneError = 'Это не номер телефона'
class messages:
    class list:
        listempty = '_Тут пока пусто_'
        description = 'Описание выступления: '
        bandname = 'Название исполнителя: '
        time = 'Время выступления: '
        login = 'Контактные данные выступающего: '

