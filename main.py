import dateutil
import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re


class FixDataFinder:    #Класс, объеденяющий в себе все функции, которые отвечают за фиксированную дату
    __months__ = [
        'января',
        'февраля',
        'марта',
        'апреля',
        "мая",
        "июня",
        "июля",
        "августа",
        "сентября",
        "октября",
        'ноября',
        'декабря']
    __week__ = ['понедельник','вторник','среду','четверг','пятницу','субботу','воскресенье']

    def year(str):   #на вход получает изначальную строку. Возвращает год
        yeartxt = ['года']
        for i in yeartxt:
            if i in str:
                return str[str.find(i) - 5:str.find(i) - 1]
        else:
            return None

    def month(str):     #на вход получает изначальную строку. Возвращает месяц
        for i in FixDataFinder.__months__:
            if i in str:
                return FixDataFinder.__months__.index(i) + 1
        return None

    def day(str):        #на вход получает изначальную строку. Возвращает день
        for i in FixDataFinder.__months__:
            if i in str:
                if str[str.find(i) - 3].isdigit():
                    return str[str.find(i) - 3:str.find(i) - 1]
                else:
                    return str[str.find(i) - 2:str.find(i) - 1]
        return None

    def time(str):      #на вход получает изначальную строку. Записывает время в окончательный словарь
        global MESSAGE
        if 'утром' in str or 'вечером' in str or 'днем' in str:
            if 'утром' in str:
                MESSAGE['DATE']['hour'] = 9
                MESSAGE['DATE']['minute'] = 0
            elif 'днем' in str:
                MESSAGE['DATE']['hour'] = 13
                MESSAGE['DATE']['minute'] = 0
            elif 'вечером' in str:
                MESSAGE['DATE']['hour'] = 19
                MESSAGE['DATE']['minute'] = 0
        elif str.rfind(':') and str[str.rfind(':')-1].isdigit() and str[str.rfind(':')+1].isdigit():
            time = str[str.rfind(':') - 2:str.rfind(':') + 3]
            if time[0] == ' ':
                MESSAGE['DATE']['hour'] = time[1:2]
                MESSAGE['DATE']['minute'] = time[3:]
            else:
                MESSAGE['DATE']['hour'] = time[:2]
                MESSAGE['DATE']['minute'] = time[3:]

    def dayOfWeek(str):
        for i in FixDataFinder.__week__:
            if i in str:
                if datetime.now().weekday()<FixDataFinder.__week__.index(i):
                    return FixDataFinder.__week__.index(i)-datetime.now().weekday()

def Delete_Date(str):
    __months__ = [
        'января',
        'февраля',
        'марта',
        'апреля',
        "мая",
        "июня",
        "июля",
        "августа",
        "сентября",
        "октября",
        'декабря']
    __week__ = ['понедельник', 'вторник', 'среду', 'четверг', 'пятницу', 'субботу', 'воскресенье']
    for i in __months__:
        if i in str:
            return str[:str.find(i)-3]
    for i in __week__:
        if i in str:
            return str[:str.find(i)-3]

    if 'через' in str:
        return str[:str.find('через')-1]
    else:
        for i in str:
            if i.isdigit():
                str=str[:str.find(i)-1]
                if str[-1]=='в' and str[-2]==' ':
                    str=str[:-2]
                return str


def dynamic_time(list):    #Используется когда используется предлог "через"
    global current_time
    if len(list)==1:
        if list[0]=='год':
            current_time += timedelta(years=1)
        elif list[0] == 'час':
            current_time += timedelta(hours=1)
        elif list[0] == 'день':
            current_time += timedelta(days=1)
        elif list[0]=='месяц':
            current_time += timedelta(months=1)
        elif list[0] == 'минуту':
            current_time += timedelta(minutes=1)
        elif list[0]=='неделю':
            current_time += timedelta(days=7)
    elif  list[1] == 'года' or list[1] == 'лет':
        current_time += timedelta(years=int(list[0]))
    elif list[1] == 'месяца' or list[1] == 'месяцев':
        current_time += timedelta(months=int(list[0]))
    elif list[1] == 'месяц':
        current_time += timedelta(months=1)
    elif list[1] == 'дня' or list[1] == 'дней':
        current_time += timedelta(days=int(list[0]))
    elif list[1] == 'день':
        current_time += timedelta(days=1)
    elif list[1] == 'часа' or list[1] == 'часов':
        current_time += timedelta(hours=int(list[0]))
    elif list[1] == 'час':
        current_time += timedelta(hours=1)
    elif list[1] == 'минут' or list[1] == 'минуты':
        current_time += timedelta(minutes=int(list[0]))
    elif list[1] == 'минуту':
        current_time += timedelta(minutes=1)


def updateDynTime(c):

    MESSAGE['DATE']['year'] = c.year
    MESSAGE['DATE']['month'] = c.month
    MESSAGE['DATE']['day'] = c.day
    MESSAGE['DATE']['hour'] = c.hour
    MESSAGE['DATE']['minute'] = c.minute


def chisla(str):  #обрабатывает запросы типа: "Приготовить плов 17 числа". И тут у меня кончилась фантазия для названий функций
    str=str[str.rfind('числа')-3:str.rfind('числа')-1]
    if str[0]==' ':
        str=str[1:]
    c = datetime.now()
    if int(str)<int(datetime.now().day):
        c += relativedelta(months=1)
        c -= relativedelta(days= c.day-int(str))
        return c
    else:
        c += timedelta(days=int(str) - c.day)
        return c

def zero_adder():
    global MESSAGE
    num=[1,2,3,4,5,6,7,8,9]
    snum=['1','2','3','4','5','6','7','8','9']
    if MESSAGE['DATE']['month'] in num or MESSAGE['DATE']['month'] in snum :
        MESSAGE['DATE']['month'] = '0' + str(MESSAGE['DATE']['month'])

    if  MESSAGE['DATE']['day'] in num or MESSAGE['DATE']['day'] in snum:
        MESSAGE['DATE']['day'] = '0' + str(MESSAGE['DATE']['day'])

    if  MESSAGE['DATE']['minute'] in num:
        MESSAGE['DATE']['minute'] = '0' + MESSAGE['DATE']['minute']

    #if MESSAGE['DATE']['hour'] in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
    #    MESSAGE['DATE']['hour'] = '0' + MESSAGE['DATE']['hour']

def space_deleter():
    global msgin
    while '  ' in msgin:
        msgin=msgin.replace('  ',' ')

def addToInt():
    global MESSAGE
    int(MESSAGE['DATE']['year'])
    int(MESSAGE['DATE']['month'])
    int(MESSAGE['DATE']['day'])
    int(MESSAGE['DATE']['hour'])
    int(MESSAGE['DATE']['minute'])

"""
def TxttoInt(str):
    list=str.split()
    for i in list:
        if 'NUMR' in morph.parse(i)[0].tag:
            list[list.index(i)]=''
"""

def datecomp():
    global MESSAGE
    c=datetime(int(MESSAGE['DATE']['year']),int(MESSAGE['DATE']['month']),int(MESSAGE['DATE']['day']),int(MESSAGE['DATE']['hour']),int(MESSAGE['DATE']['minute']))

    if c>datetime.now():
        return True
    else:
        return False

msgin = input()

space_deleter()

MESSAGE = {'STATUS': None, 'DATE': {'year': None, 'month': None, 'day': None, 'hour': None, 'minute': None},
           'TEXT': None}

if 'через' in msgin:                            #здесь происходит обработка сообщения с предлогом через
    str = msgin[msgin.rfind('через') + 6:]
    list = str.split(' ')
    current_time = datetime.now()
    while list:
        dynamic_time(list[:2])
        list.remove(list[0])
        if list:
            list.remove(list[0])
    updateDynTime(current_time)

elif 'завтра' in msgin or 'послезавтра' in msgin:
    current_time = datetime.now()
    if 'завтра' in msgin:
        current_time += timedelta(days=1)
    if 'послезавтра' in msgin:
        current_time += timedelta(days=2)
    updateDynTime(current_time)


elif 'числа' in msgin:
    c=chisla(msgin)
    updateDynTime(c)

elif 'понедельник' in msgin or'вторник' in msgin or 'среду' in msgin or 'четверг' in msgin or 'пятницу' in msgin or 'субботу' in msgin or'воскресенье' in msgin:
    current_time = datetime.now()
    current_time+= relativedelta(days=FixDataFinder.dayOfWeek(msgin))
    updateDynTime(current_time)
    FixDataFinder.time(msgin)


else:
    MESSAGE['DATE']['year'] = FixDataFinder.year(msgin)
    MESSAGE['DATE']['month'] =FixDataFinder.month(msgin)
    MESSAGE['DATE']['day'] = FixDataFinder.day(msgin)
    FixDataFinder.time(msgin)


    if not MESSAGE['DATE']['year']:
        MESSAGE['DATE']['year']=datetime.now().year
    if not MESSAGE['DATE']['month']:
        MESSAGE['DATE']['month'] = datetime.now().month
    if not MESSAGE['DATE']['day']:
        MESSAGE['DATE']['day'] = datetime.now().day
        if not datecomp():
            MESSAGE['DATE']['day']+=1

MESSAGE['TEXT'] = Delete_Date(msgin)

print(MESSAGE)

#print("Напоминание записано!", '\n', MESSAGE['TEXT'], '\n', 'Выполнить в ', MESSAGE['DATE']['hour'], ':',MESSAGE['DATE']['minute'], ' ', MESSAGE['DATE']['day'], '.', MESSAGE['DATE']['month'], '.',MESSAGE['DATE']['year'], sep='')



"""
Created by Iskatel_capitan
"""