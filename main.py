import datetime
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import re



class Parser:
    months = [
        'января',
        'февраля',
        'марта',
        'апреля',
        'мая',
        'июня',
        'июля',
        'августа',
        'сентября',
        'октября',
        'ноября',
        'декабря']
    week = ['понедельник','вторник','среду','четверг','пятницу','субботу','воскресенье']

    def __init__(self, message):
        self.raw_message = message
        self.year = 0
        self.month = None
        self.day = None
        self.hour = None
        self.minute = None
        self.text = None
        self.DayOfWeek = None
        self.repeatAlways = None
        self.status = None



        try:
            if re.search('\d\d.\d\d.\d{4}', message) or re.search('\d\d.\d\d.\d{2}', message):
                if re.search('\d\d.\d\d.\d{4}', message):
                    r = re.search('\d\d.\d\d.\d{4}', message)
                else:
                    r = re.search('\d\d.\d\d.\d{2}', message)
                self.day = r[0][:2]
                self.month = r[0][3:5]
                self.year = r[0][6:]
                self.text = self.Delete_Date(message)

            if re.search('\d\d-\d\d-\d{4}', message) or re.search('\d\d-\d\d-\d{2}', message):
                if re.search('\d\d-\d\d-\d{4}', message):
                    r = re.search('\d\d-\d\d-\d{4}', message)
                else:
                    r = re.search('\d\d-\d\d-\d{2}', message)
                self.day = r[0][:2]
                self.month = r[0][3:5]
                self.year = r[0][6:]
                self.text = self.Delete_Date(message)


            if re.search('\d\d:\d\d', message):
                r = re.search('\d\d:\d\d', message)
                self.hour = r[0][:2]
                self.minute = r[0][3:]

            if re.search(' \d:\d\d', message):
                r = re.search(' \d:\d\d', message)
                self.hour = r[0][1:2]
                self.minute = r[0][3:]

            if 'кажд' in message or "Кажд" in message:
                if "каждый" in message or " Каждый" in message:
                    if "день" in message:
                        self.repeatAlways = 'day'
                    elif 'месяц' in message:
                        self.repeatAlways = 'month'
                    elif 'год' in message:
                        self.repeatAlways = 'year'
                    elif 'час' in message:
                        self.repeatAlways = 'hour'
                    elif 'понедельник' in message:
                        self.repeatAlways = 'monday'
                    elif 'вторник' in message:
                        self.repeatAlways='tuesday'
                    elif "четверг" in message:
                        self.repeatAlways='thursday'
                elif "каждое" in message or " Каждое" in message:
                    if 'число' in message:
                        self.day = message[message.find('число')-3:message.find('число')]
                        if self.day[0] == ' ':
                            self.day = self.day[1:]
                        if self.day[-1] == ' ':
                            self.day = self.day[:-1]
                        self.repeatAlways = 'month'
                    elif "Воскресенье" in message:
                        self.repeatAlways = 'sunday'
                    elif "утро" in message:
                        self.repeatAlways = 'day'
                        self.hour = 9
                        self.minute = 0
                elif "каждую" in message:
                    if "среду" in message:
                        self.repeatAlways ='wednesday'
                    elif 'пятницу' in message:
                        self.repeatAlways ='friday'
                    elif 'субботу' in message:
                        self.repeatAlways ='saturday'
                    elif "неделю" in message:
                        self.repeatAlways ='week'
                if "каждые" in message:
                    if "выходные" in message:
                        self.repeatAlways = 'weekends'
                self.text = self.Delete_Date(message)


            elif 'через' in message or 'Через' in message:  # здесь происходит обработка сообщения с предлогом через
                string = message[message.rfind('через') + 6:]
                if string[0] == ' ':
                    string = string[1:]
                List = string.split(' ')
                current_time = datetime.now()
                while List:
                    current_time = self.dynamic_time(List[:2],current_time)
                    List.remove(List[0])
                    if List and not List[0].isdigit():
                        List.remove(List[0])
                self.updateDynTime(current_time)

            elif 'завтра' in message or 'послезавтра' in message:
                current_time = datetime.now()
                if 'завтра' in message:
                    current_time += timedelta(days=1)
                if 'послезавтра' in message:
                    current_time += timedelta(days=2)
                self.updateDynTime(current_time)
                self.text = self.Delete_Date(message)


            elif 'числа' in message:
                c = self.chisla(message)
                self.updateDynTime(c)

            elif 'понедельник' in message or 'вторник' in message or 'среду' in message or 'четверг' in message or 'пятницу' in message or 'субботу' in message or 'воскресенье' in message:
                self.DayOfWeek = self.dayOfWeek(message)+1
                cur = datetime.now()
                cur += timedelta(days=self.DayOfWeek)
                self.day = cur.day
                self.month = cur.month
                if not self.hour and not self.minute:
                    self.hour = datetime.now().hour
                    self.minute = datetime.now().minute

            else:
                self.year = self.YearFinder(message)
                self.month = self.MonthFinder(message)
                self.day = self.DayFinder(message)
                self.Time(message)
                self.Time(message)



            if not self.year and not self.repeatAlways:
                self.year = datetime.now().year
                try:
                    if not self.datecomp():
                        self.year += 1
                except:
                    pass
            if not self.month and not self.repeatAlways:
                self.month = datetime.now().month
            if not self.day and not self.repeatAlways:
                self.day = datetime.now().day
                if not self.datecomp():
                    self.day += 1
            if not self.hour:
                self.hour = datetime.now().hour
            if not self.minute:
                self.minute = 0
            self.text = self.Delete_Date(message)
            #self.text = self.Delete_Date(self.text)
            self.status = 'SUCCESS'
            if self.text[-1] == ' ':
                self.text = self.text[:-1]
        except Exception as e:
            pass
            self.status = 'ERROR'
            self.text = e



    def Print_info(self):
        if self.repeatAlways:
            MESSAGE = {'STATUS': self.status,'DATE': {'hour': self.hour, 'minute': self.minute},
                       'PARAMS': {"REPEAT_ALWAYS":self.repeatAlways},
                       'TEXT': self.text, 'raw_text': self.raw_message}
            if self.day:
                MESSAGE['DATE']['day'] = self.day
        else:
            MESSAGE = {'STATUS':self.status, 'DATE': {'year': self.year, 'month': self.month, 'day': self.day, 'hour': self.hour, 'minute': self.minute},
                   'TEXT': self.text,'raw_text':self.raw_message}
        print(0)
        return MESSAGE


    def YearFinder(self,string):   #на вход получает изначальную строку. Возвращает год
        yeartxt = ['года']
        for i in yeartxt:
            if i in string:
                return string[string.find(i) - 5:string.find(i) - 1]
        else:
            return None

    def MonthFinder(self,string):     #на вход получает изначальную строку. Возвращает месяц
        for i in self.months:
            if i in string:
                return self.months.index(i) + 1
        return None

    def DayFinder(self,string):        #на вход получает изначальную строку. Возвращает день
        for i in self.months:
            if i in string:
                if string[string.find(i) - 3].isdigit():
                    return string[string.find(i) - 3:string.find(i) - 1]
                else:
                    return string[string.find(i) - 2:string.find(i) - 1]
        return None

    def Time(self,string):      #на вход получает изначальную строку. Записывает время в окончательный словарь
        if not self.hour and not self.minute:
            if 'утром' in string or 'вечером' in string or 'днем' in string:
                if 'утром' in string:
                    self.hour = 9
                    self.minute = 0
                elif 'днем' in string:
                        self.hour = 13
                        self.minute = 0
                elif 'вечером' in string:
                        self.hour = 19
                        self.minute = 0

    def dayOfWeek(self, string):
        for i in self.week:
            if i in string:
                if datetime.now().weekday() < self.week.index(i):
                    return self.week.index(i)-datetime.now().weekday()
                else:
                    return (6-datetime.now().weekday())+self.week.index(i)

    def dayOfWeek2(self, string):
        for i in self.week:
            if i in string:
                return self.week.index(i)


        """week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        for i in week:
            if i in string:
                return week[self.week.index(i)]"""



    def Delete_Date(self, string):

        for i in self.months:
            if i in string:
                return string[:string.find(i)-3]
        for i in self.week:
            if i in string:
                return string[:string.find(i)-3]
        if 'кажд' in string:
            f = string.split()
            for i in f:
                if 'кажд' in i:
                    try:
                        if f[f.index(i)+2]=='число':
                            del f[f.index(i):f.index(i) + 3]
                        else:
                            del f[f.index(i):f.index(i) + 2]
                    except:
                        del f[f.index(i):f.index(i)+2]

                    return ' '.join(f)
        if 'через' in string or 'Через' in string:
            a = ['день','года','лет','месяца','месяцев','месяц' ,'дня','дней','часа','часов','час','минут','минуты','минуту','недель']
            if string.find('через') == 0 or string.find('Через') == 0:
                for i in a:
                    if i in string:
                        string = string[string.find(i)+len(i):]
                return string
            else:
                return string[:string.find('через')-1]
        else:
            for i in string:
                if i.isdigit():
                    string = string[:string.find(i)-1]
                    if string[-1] == 'в' and string[-2] == ' ':
                        string = string[:-2]
                    return string

        if 'послезавтра' in string:
            return string[:string.find('послезавтра')-1]
        elif 'завтра' in string:
            return string[:string.find('завтра')-1]

        if re.search('\d\d.\d\d.\d{4}', string) or re.search('\d\d.\d\d.\d{2}', string):
            if re.search('\d\d.\d\d.\d{4}', string):
                r = re.search('\d\d.\d\d.\d{4}', string)
            else:
                r = re.search('\d\d.\d\d.\d{2}', string)
            return string[:r.start()]

        if re.search('\d\d:\d\d', string):
            r = re.search('\d\d:\d\d', string)
            return string[:r.start() - 2] + string[r.end():]

        if re.search('\d:\d\d', string):
            r = re.search('\d:\d\d', string)
            return string[:r.start() - 2] + string[r.end():]





    def dynamic_time(self,List,current_time):    #Используется когда используется предлог "через"
        if not List[0].isdigit():
            if List[0] == 'год':
                current_time += relativedelta(years=1)
            elif List[0] == 'час':
                current_time += timedelta(hours=1)
            elif List[0] == 'день':
                current_time += timedelta(days=1)
            elif List[0]=='месяц':
                current_time += relativedelta(months=1)
            elif List[0] == 'минуту':
                current_time += timedelta(minutes=1)
            elif List[0]=='неделю':
                current_time += timedelta(days=7)
        elif List[1] == 'года' or list[1] == 'лет':
            current_time += relativedelta(years=int(List[0]))
        elif List[1] == 'месяца' or list[1] == 'месяцев':
            current_time += relativedelta(months=int(List[0]))
        elif List[1] == 'месяц':
            current_time += relativedelta(months=1)
        elif List[1] == 'дня' or List[1] == 'дней':
            current_time += timedelta(days=int(List[0]))
        elif List[1] == 'день':
            current_time += timedelta(days=1)
        elif List[1] == 'часа' or list[1] == 'часов':
            current_time += timedelta(hours=int(List[0]))
        elif List[1] == 'час':
            current_time += timedelta(hours=1)
        elif List[1] == 'минут' or list[1] == 'минуты':
            current_time += timedelta(minutes=int(List[0]))
        elif List[1] == 'минуту':
            current_time += timedelta(minutes=1)
        elif List[1] == 'недель':
                current_time += timedelta(days=7*int(List[0]))
        return current_time
    def updateDynTime(self,c):

        self.year = c.year
        self.month = c.month
        self.day = c.day
        if not self.hour:
            self.hour = c.hour
        if not self.minute:
            self.minute = c.minute


    def chisla(self,string):  #обрабатывает запросы типа: "Приготовить плов 17 числа". И тут у меня кончилась фантазия для названий функций
        string = string[string.rfind('числа')-3:string.rfind('числа')-1]
        if string[0] == ' ':
            string = string[1:]
        c = datetime.now()
        if int(string) < int(datetime.now().day):
            c += relativedelta(months=1)
            c -= relativedelta(days=c.day-int(string))
            return c
        else:
            c += timedelta(days=int(string) - c.day)
            return c



    def datecomp(self):
        c = datetime(int(self.year),int(self.month),int(self.day),int(self.hour),int(self.minute))
        if c > datetime.now():
            return True
        else:
            return False


pars1 = Parser(input())
print(pars1.Print_info())





"""
Created by Iskatel_capitan
"""