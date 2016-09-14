
from pymjin2 import *

class TimerImpl(object):
    def __init__(self, c):
        self.c = c
        self.seconds = []
        self.minutes = 0
        self.time = []
        self.clock = []
    def __del__(self):
        self.c = None
    def addClock(self, key, value):
        timeNum=len(self.clock)+1
        timeName='time'+str(timeNum)
        self.clock.append(timeName)
        print(self.clock)
    def onTick1(self, key, value):
        if len(self.seconds)<1:
            self.seconds.append(0)
        self.seconds[0] = self.seconds[0] + 1
        if self.seconds[0] == 60:
            self.minutes = self.minutes + 1
            self.seconds[0] = 0
            sec = str(self.seconds[0])
        if len(str(self.seconds[0])) < 2:
            sec = '0' + str(self.seconds[0])
        else:
            sec = str(self.seconds[0])
        if len(str(self.minutes)) > 1:
            sec = str(self.seconds[0])[:1]
        time = str(self.minutes) + '-' + sec
        #print('%s=%s' %(self.time[0], time))
        print('time1=%s' %time)
    def onTick2(self, key, value):
        if len(self.seconds)<2:
            self.seconds.append(0)
        self.seconds[1] = self.seconds[1] + 1
        if self.seconds[1] == 60:
            self.minutes = self.minutes + 1
            self.seconds[1] = 0
            sec = str(self.seconds[0])
        if len(str(self.seconds[1])) < 2:
            sec = '0' + str(self.seconds[1])
        else:
            sec = str(self.seconds[1])
        if len(str(self.minutes)) > 1:
            sec = str(self.seconds[1])[:1]
        time = str(self.minutes) + '-' + sec
        #print('%s=%s' %(self.time[0], time))
        print('time2=%s' %time)

class Timer(object):
    def __init__(self, sceneName, nodeName, env):
        self.c = EnvironmentClient(env, "Timer/" + nodeName)
        self.impl = TimerImpl(self.c)
        self.c.listen("timer.clock1.tick", None, self.impl.onTick1)
        self.c.set("timer.clock1.timeout", "1000")
        self.c.set("timer.clock1.enabled", "1")
        self.c.listen("timer.clock1.enabled", None, self.impl.addClock)
        self.c.listen("timer.clock2.tick", None, self.impl.onTick2)
        self.c.set("timer.clock2.timeout", "2000")
        self.c.set("timer.clock2.enabled", "1")
        self.c.listen("timer.clock2.enabled", None, self.impl.addClock)
    def __del__(self):
        self.c.clear()
        del self.impl
        del self.c

def SCRIPT_CREATE(sceneName, nodeName, env):
    return Timer(sceneName, nodeName, env)

def SCRIPT_DESTROY(instance):
    del instance
