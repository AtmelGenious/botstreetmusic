from webbrowser import get


pointNames = ['Сцена (Кинотеатр Беларусь)', 'Пятачок (ТЦ "Миллионный")', 'ТЦ "Дидас Персия"']
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
        button2 = '🗺Управление выступлениями'
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
quotes = ['-Музыка — это посредник между духовной и чувст­венной жизнью. \n    Б. Арним', 'Я очень сожалел бы, если бы моя музыка только развлекала моих слушателей: я стремился их сделать лучше. \n    Г.Гендель', 'От музыки зависит очень много: настроение, пульс, температура и дальнейшие действия.', 'Если вы действительно любите музыку, то вам не должно быть стыдно за ту музыку, которую вы любите. \n    Джерард Артур Уэй', 'У меня нет друзей... Зато есть номер барыги!!! \n    Юрий Каплан', 'Рок — это музыка, посредством которой можно разобраться в своем внутреннем мире и отыскать частичку себя, не убив при этом никого. \n    Джаред Лето', 'Если мелодию невозможно запомнить сразу, то она никуда не годится.\n    Джузеппе Верди', 'Не царское это дело — музыку тихо слушать.', 'Я не знаю, существует ли хоть один великий музыкант, о котором можно было бы сказать, что он устарел.', 'Те, кого видели танцующими, казались безумными тем, кто не мог слышать музыку. \n    Фридрих Ницше']