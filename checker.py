import paramiko
import time
from threading import Thread
from writer_reader import fileManager


class sshManager(Thread):
    def __init__(self, botObject=None):
        super().__init__()
        self.botObject = botObject
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def setEditer(self, func1, func2, func3):
        self.funcGoodHosts = func1
        self.funcBadHosts = func2
        self.funcPolling = func3

    def checkAllHost(self):
        self.funcPolling()
        manager = fileManager()
        listHost = manager.getAllHosts()
        goodHosts = []
        badHosts = []
        for host in listHost:
            try:
                self.client.connect(
                    hostname=host[1], username=host[2], password=host[3], port=22
                )
                self.client.close()
                print(host[0])
                goodHosts.append([host[0], host[1]])
            except Exception:
                badHosts.append([host[0], host[1]])

        self.funcGoodHosts(goodHosts)
        self.funcBadHosts(badHosts)

    def run(self):
        while True:
            self.checkAllHost()
            time.sleep(600)
