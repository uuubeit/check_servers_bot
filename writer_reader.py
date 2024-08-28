class fileManager(object):
    def addHost(self, msg):
        self.file = open("hosts.txt", "r+")
        try:
            listMsg = msg.split("\n")
        except Exception:
            return 0
        for line in listMsg:
            if len(line.split("/")) == 4:
                self.file.seek(0, 2)
                self.file.write(line + "\n")
            else:
                self.file.close()
                return 0
        self.file.close()
        return 1

    def getAllHosts(self) -> list:
        self.file = open("hosts.txt", "r+")
        hostsDict = []
        data = self.file.readlines()
        for line in data:
            listLine = line[:-1].split("/")
            hostsDict.append([listLine[0], listLine[1], listLine[2], listLine[3]])
        self.file.close()
        return hostsDict

    def delHost(self, name=str):
        self.file = open("hosts.txt", "r+")
        data = self.file.readlines()
        for index in range(len(data)):
            if data[index][: len(name)] == name:
                data.pop(index)
                self.file.truncate(0)
                self.file.seek(0)
                tim = "".join(data)
                self.file.write(tim)
                self.file.close()
                return True
        self.file.close()
        return False
