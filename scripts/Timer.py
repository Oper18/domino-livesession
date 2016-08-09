
from pymjin2 import *

LCD_MATERIAL_NAME_PREFIX = "lcd_digit"

class TimerImpl(object):
    def __init__(self, c):
        self.c = c
        self.digits = []
        self.seconds = 0
        self.minutes = 0
        self.time = 0
    def __del__(self):
        self.c = None
    def locateDigitNodesOnce(self):
        # Only do it once.
        if (len(self.digits)):
            return
        # Children are digits.
        self.digits = self.c.get("node.$SCENE.$NODE.children")
    def onTick(self, key):
        print('tick1')
        self.seconds = self.seconds + 1
        print('tick2')
        if self.seconds == 60:
            print('tick2.1')
            self.minutes = self.minutes + 1
            print('tick2.2')
            self.seconds = 0
        print('tick3')
        time = str(self.minutes) + '-' + str(self.seconds)
        print('tick4')
        #self.c.set("timer.clock.tick", time)
        print('tick5')
        #self.c.unlisten("timer.clock.tick")
        #self.c.report("timer.setTime", "0")
        return [str(time)]
    def setDigitValue(self, digitID, value):
        self.c.setConst("DIGIT", self.digits[digitID])
        material = LCD_MATERIAL_NAME_PREFIX + value
        self.c.set("node.$SCENE.$DIGIT.material", material)
    '''def setTime(self, key):
        print('timer1')
        self.c.listen("timer.clock.tick", None, self.onTick)
        print('timer2')
        #self.onTick(key)
        self.c.set("timer.clock.timeout", "1000")
        print('timer3')
        self.c.set("timer.clock.enabled", "1")
        print('timer4')
        return [str(self.time)]'''
    def setValue(self, key, value):
        self.locateDigitNodesOnce()
        strval = value[0]
        # Display nothing if:
        # * Value is longer than we can display.
        # * Value is none.
        if ((len(strval) > len(self.digits)) or
            not len(strval)):
            for i in xrange(0, len(self.digits)):
                self.setDigitValue(i, "")
            return
        # Divide string value into separate digits.
        # Use empty value for padded digits.
        start = len(self.digits) - len(strval)
        for i in xrange(0, len(self.digits)):
            # Digit.
            if (i >= start):
                self.setDigitValue(i, strval[i - start])
            # Padding.
            else:
                self.setDigitValue(i, "")

class Timer(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Timer/" + nodeName)
        self.impl = TimerImpl(self.c)
        self.c.setConst("SCENE",  sceneName)
        self.c.setConst("NODE",   nodeName)
        self.c.listen("timer.clock.tick", None, self.impl.onTick)
        self.c.provide("timer.$SCENE.$NODE.value", self.impl.setValue)
        #self.c.provide("timer.setTime", None, self.impl.setTime)
        self.c.provide("timer.tick", None, self.impl.onTick)
    def __del__(self):
        # Tear down.
        self.c.clear()
        # Destroy.
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Timer(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance

