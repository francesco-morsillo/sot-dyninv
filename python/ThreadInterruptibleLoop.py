import signal, threading, time

class ThreadInterruptibleLoop(threading.Thread):
    isQuit=False
    isPlay=False
    sleepTime=1e-3
    previousHandler = None
    isOnce=0
    isRunning=False
    iter=0

    def __init__(self):
        threading.Thread.__init__(self)
        self.setSigHandler()

    def quit(self): self.isQuit = True
    def setPlay(self,mode):
        self.isPlay = mode
    def play(self):
        if not self.isRunning: self.start()
        self.isOnce = False
        self.setPlay(True)
    def pause(self): self.setPlay(False)
    def once(self):
        self.isOnce=True
        self.setPlay(True)
    def run(self):
        self.isQuit=False
        self.isRunning=True
        while not self.isQuit:
            if self.isPlay:
                self.loop()
                self.iter+=1
                if self.isOnce: self.pause()
            time.sleep(self.sleepTime)
        self.isRunning=False
        print 'Thread loop will now end.'

    def sigHandler(self,signum, frame):
        print 'Catch signal ', signum
        signal.signal(signum, self.previousHandler)
        self.quit()
    def setSigHandler(self):
        self.previousHandler = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, (lambda x,y: self.sigHandler(x,y)) )

    def start(self):
        self.setPlay(True)
        threading.Thread.start(self)
    def restart(self):
        self.join()
        self.play()
        self.setSigHandler()
        threading.Thread.start(self)
    def loop(self):
        None



# To use the previous class, a 'loop' function has to be define.
# Everything will be embedded by using the decorator below. Just
# use it as:
#   >>> @loopInThread
#   >>> def Runner():
#   >>>    to what you want here
#   >>> runner = Runner()
#   >>> runner.pause()/play()/quit() ...
def loopInThread( funLoop ):
    class ThreadViewer(ThreadInterruptibleLoop):
        def __init__(self):
            ThreadInterruptibleLoop.__init__(self)
#            self.start()
        def loop(self):
            funLoop()
    return ThreadViewer
