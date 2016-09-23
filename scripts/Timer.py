
from pymjin2 import *

class TimerImpl(object):
    def __init__(self, c):
        self.c = c
        self.seconds = 0
        self.minutes = 0
    def __del__(self):
        self.c = None
    def onSpace(self, key, value):
        self.c.set("timer.clock$NUMBER.enabled", "1")
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
        print('time1=%s' %time)

class Timer(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Timer/" + nodeName)
        self.impl = TimerImpl(self.c)
        #self.timeTick = [1000, 2000]
        num = nodeName[5:]
        num = int(num)
        timeTick=num*1000
        self.c.setConst("NUMBER", str(num))
        self.c.listen("timer.clock%d.tick" %num, None, self.impl.onTick)
        self.c.set("timer.clock%d.timeout" %num, "%d" %timeTick)
        #self.c.set("timer.clock%d.timeout" %num, "%d" %self.timeTick[num-1])
        self.c.listen("input.SPACE.key", "1", self.impl.onSpace)
    def __del__(self):
        self.c.clear()
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Timer(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance
