
from pymjin2 import *

#ссылка на материал
TIMER_MATERIAL_NAME_PREFIX = "lcd_digit"

#Класс с действиями
class TimerImpl(object):
    #Конструктор класса 
    def __init__(self, c):
        #Аргумент передаваемый в конструктор при вызове
        self.c = c
        #Создание списка фишек
        self.digits = []
        #Создание переменной отвечающей за секунды
        self.seconds = 0
        #Создание переменной отвечающей за минуты
        self.minutes = 0
    #Деструктор
    def __del__(self):
        #Уничтожение ссылки на конструктор
        self.c = None
    #Метод получает длину списка фишек
    def locateDigitNodesOnce(self):
        # Only do it once.
        #Считывает длину списка фишек
        if (len(self.digits)):
            #Возвращает None
            return
        # Children are digits.
        #В self.digits передаются значения фишек
        self.digits = self.c.get("node.$SCENE.$NODE.children")
    #Отсчет времени
    def onTick(self, key, value):
        #Увеличение секунд на 1 каждый раз когда вызывается функция - отсчет времени
        self.seconds = self.seconds + 1
        #Проверка количества секунд, если секунд 60, минуты увеличиваются а секунды обнуляются
        if self.seconds == 60:
            #Увеличение минут на 1
            self.minutes = self.minutes + 1
            #Обнуление секунд
            self.seconds = 0
            #Установка секунд в строку для передачи времени в таймер
            sec = str(self.seconds)
        #Проверка длины секунд (меньше 2) для отображения м-0с если секунд меньше 10
        if len(str(self.seconds)) < 2:
            #Установка 0 перед секундой
            sec = '0' + str(self.seconds)
        #Проверка длины секунды (если не 1) для отображения м-сс если секунд больше 10
        else:
            #Установка секунд в том виде как есть
            sec = str(self.seconds)
        #Проверка длины минут (больше 1) для перехода от отображения м-сс к мм-с
        if len(str(self.minutes)) > 1:
            #установка десятков секунд и отброс единиц
            sec = str(self.seconds)[:1]
        #Установка переменной времени с текстом который отобразтся на дисплее
        time = str(self.minutes) + '-' + sec
        #Печать переменной времени
        print('time=%s' %time)
        #return [str(time)]
    #Функция значения фишек
    def setDigitValue(self, digitID, value):
        #Установка константы DIGIT (присваивается значение текущей фишки) для передачи ее в set
        self.c.setConst("DIGIT", self.digits[digitID])
        #Создание переменной (материал+цифра=имя материала) для передачи ее в set
        material = TIMER_MATERIAL_NAME_PREFIX + value
        #Установка ключа
        self.c.set("node.$SCENE.$DIGIT.material", material)
    #Функция значения
    def setValue(self, key, value):
        #Вызов функции
        self.locateDigitNodesOnce()
        #Создание переменной (первый элемент из списка value)
        strval = value[0]
        # Display nothing if:
        # * Value is longer than we can display.
        # * Value is none.
        #Проверка длины strval и наличия переменной чтобы оставить дисплей пустым при длине большей чем можем отобразить или если value не задано 
        if ((len(strval) > len(self.digits)) or
            not len(strval)):
            #Цикл по длине списка self.digits для проверки каждой фишки
            for i in xrange(0, len(self.digits)):
                #Вызов функции и передача значений (digitID=номер текущей итерации, None)
                self.setDigitValue(i, "")
            #Возвращает значение None
            return
        # Divide string value into separate digits.
        # Use empty value for padded digits.
        #Создание переменной длина self.digits - длина переменной strval для задания значения None для value для пустых слотов
        start = len(self.digits) - len(strval)
        #Цикл по длине списка self.digits
        for i in xrange(0, len(self.digits)):
            # Digit.
            #Условие номер итерации больше значения переменной для определения наличия фишки в слоте
            if (i >= start):
                #Вызов функции с параметрами (номер итерации, переменная)
                self.setDigitValue(i, strval[i - start])
            # Padding.
            #Иначе
            else:
                #Вызов функции с параметрами (номер итерации, None)
                self.setDigitValue(i, "")

#Класс с данными
class Timer(object):
    #Конструктор класса
    def __init__(self, sceneName, nodeName, env):
        #Создаём клиента окружения
        self.c = EnvironmentClient(env, "Timer/" + nodeName)
        #Создание ссылки  на класс TimerImpl для обращения к методам этого класса извне
        self.impl = TimerImpl(self.c)
        #Создание константы SCENE для передачи в key для создания ID 
        self.c.setConst("SCENE",  sceneName)
        #Создание константы NODE для передачи в key для создания ID
        self.c.setConst("NODE",   nodeName)
        #При прохождении указанного времени в таймере clock вызывается функция
        self.c.listen("timer.clock.tick", None, self.impl.onTick)
        #Устанавливается кол-во времени в таймер clock после которого будет вызвана функция
        self.c.set("timer.clock.timeout", "1000")
        #Запуск таймера, называющегося clock
        self.c.set("timer.clock.enabled", "1")
        #Создание ссылки timer.$SCENE.$NODE.value (timer.имя сцены.имя узла.value, где имя сцены и имя узла заданы выше, а value координаты объекта) для обращения к функции извне
        self.c.provide("timer.$SCENE.$NODE.value", self.impl.setValue)
        #Создание ссылки для обращения к функции к функции onTick извне
        self.c.provide("timer.tick", None, self.impl.onTick)
    #Деструктор класса
    def __del__(self):
        # Tear down.
        #Освобождение имени self.c
        self.c.clear()
        # Destroy.
        #Удаление двух переменных
        del self.impl
        del self.c

#Функция (через нее обращается программа)
def SCRIPT_CREATE(sceneName, nodeName, env):
    #Возвращает класс Timer
    return Timer(sceneName, nodeName, env)

#Функция (что то служебное)
def SCRIPT_DESTROY(instance):
    #Уничтожение параметра instance 
    del instance

