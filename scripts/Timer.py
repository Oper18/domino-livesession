
from pymjin2 import *

TIMER_MATERIAL_NAME_PREFIX = "lcd_digit"

class TimerImpl(object):
    def __init__(self, c):
        self.c = c
        self.digits = []
        self.seconds = 0
        self.minutes = 0
    def __del__(self):
        self.c = None
    def locateDigitNodesOnce(self):
        if (len(self.digits)):
            return
        self.digits = self.c.get("node.$SCENE.$NODE.children")
    def onTick(self, key, value):
        self.seconds = self.seconds + 1
        if self.seconds == 60:
            self.minutes = self.minutes + 1
            self.seconds = 0
            sec = str(self.seconds)
        if len(str(self.seconds)) < 2:
            sec = '0' + str(self.seconds)
        else:
            sec = str(self.seconds)
        if len(str(self.minutes)) > 1:
            sec = str(self.seconds)[:1]
        time = str(self.minutes) + '-' + sec
        print('time=%s' %time)
    def setValue(self, key, value):
        self.locateDigitNodesOnce()
        strval = value[0]
        if ((len(strval) > len(self.digits)) or
            not len(strval)):
            for i in xrange(0, len(self.digits)):
                self.setDigitValue(i, "")
            return
        start = len(self.digits) - len(strval)
        for i in xrange(0, len(self.digits)):
            if (i >= start):
                self.setDigitValue(i, strval[i - start])
            else:
                self.setDigitValue(i, "")

class Timer(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Timer/" + nodeName)
        self.impl = TimerImpl(self.c)
        self.c.setConst("SCENE",  sceneName)
        self.c.setConst("NODE",   nodeName)
        self.c.listen("timer.clock.tick", None, self.impl.onTick)
        self.c.set("timer.clock.timeout", "1000")
        self.c.set("timer.clock.enabled", "1")
    def __del__(self):
        self.c.clear()
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Timer(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance
