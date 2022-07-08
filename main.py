from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
import pymorphy2
morph = pymorphy2.MorphAnalyzer()
msgin = input()


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
        'декабря']

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
                return str[str.find(i) - 3:str.find(i) - 1]
        return None

    def time(str):      #на вход получает изначальную строку. Записывает время в окончательный словарь
        if str.rfind(':') and str[str.rfind(':')-1].isdigit() and str[str.rfind(':')+1].isdigit():
            time = str[str.rfind(':') - 2:str.rfind(':') + 3]
            global MESSAGE
            if time[0] == ' ':
                MESSAGE['DATE']['hour'] = time[1:2]
                MESSAGE['DATE']['minute'] = time[3:]
            else:
                MESSAGE['DATE']['hour'] = time[:2]
                MESSAGE['DATE']['minute'] = time[3:]

def Delete_Date(str):

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

    if not list[0].isdigit():
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
    if  list[1] == 'года' or list[1] == 'лет':
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
"""
def TxttoInt(str):
    list=str.split()
    for i in list:
        if 'NUMR' in morph.parse(i)[0].tag:
            list[list.index(i)]=''
"""
MESSAGE = {'STATUS': None, 'DATE': {'year': None, 'month': None, 'day': None, 'hour': None, 'minute': None},
           'TEXT': None}

if 'через' in msgin:
    str = msgin[msgin.rfind('через') + 6:]
    list = str.split(' ')
    current_time = datetime.now()
    while list:
        dynamic_time(list[:2])
        list.remove(list[0])
        list.remove(list[0])
    print(type(current_time))
    updateDynTime(current_time)


else:
    MESSAGE['DATE']['year'] = FixDataFinder.year(msgin)
    if FixDataFinder.month(msgin) in [1,2,3,4,5,6,7,8,9]:
        MESSAGE['DATE']['month'] = '0' + str(FixDataFinder.month(msgin))
    else:
        MESSAGE['DATE']['month'] = str(FixDataFinder.month(msgin))

    if FixDataFinder.day(msgin)[0]==' ':
        MESSAGE['DATE']['day'] = '0'+FixDataFinder.day(msgin)[1]
    else:
        MESSAGE['DATE']['day'] =FixDataFinder.day(msgin)
    FixDataFinder.time(msgin)
MESSAGE['TEXT'] = Delete_Date(msgin)

'''if MESSAGE['DATE']['day'] in [1,2,3,4,5,6,7,8,9] and MESSAGE['DATE']['month'] in [1,2,3,4,5,6,7,8,9]:
    print("Напоминание записано!", '\n', MESSAGE['TEXT'], '\n', 'Выполнить в ', MESSAGE['DATE']['hour'], ':',
          MESSAGE['DATE']['minute'], ' 0', MESSAGE['DATE']['day'], '.0', MESSAGE['DATE']['month'], '.',
          MESSAGE['DATE']['year'], sep='')

elif MESSAGE['DATE']['day']<10:
    print("Напоминание записано!", '\n', MESSAGE['TEXT'], '\n', 'Выполнить в ', MESSAGE['DATE']['hour'], ':',
          MESSAGE['DATE']['minute'], ' 0', MESSAGE['DATE']['day'], '.', MESSAGE['DATE']['month'], '.',
          MESSAGE['DATE']['year'], sep='')

elif MESSAGE['DATE']['month']<10:
    print("Напоминание записано!", '\n', MESSAGE['TEXT'], '\n', 'Выполнить в ', MESSAGE['DATE']['hour'], ':',
          MESSAGE['DATE']['minute'], ' ', MESSAGE['DATE']['day'], '.0', MESSAGE['DATE']['month'], '.',
          MESSAGE['DATE']['year'], sep='')

else:'''
print("Напоминание записано!", '\n', MESSAGE['TEXT'], '\n', 'Выполнить в ', MESSAGE['DATE']['hour'], ':',MESSAGE['DATE']['minute'], ' ', MESSAGE['DATE']['day'], '.', MESSAGE['DATE']['month'], '.',MESSAGE['DATE']['year'], sep='')



"""
Created by Iskatel_capitan
"""