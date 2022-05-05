
class CnpjManager:
    def __init__(self, aFileName):
        self.position = -1
        self.list = []
        self.fileName = aFileName
        self.EOF = True

    def load(self):
        try:
            self.list = []
            self.position = -1
            if self.fileName:
                with open(self.fileName, "r") as f:
                    for line in f:
                        self.list.append(line.strip().replace('"', ''))
            self.EOF = bool(self.list)
            self.list.sort()
        except:
            pass
            # print('s1')

    def size(self):
        return self.list.__len__()

    def loadByRange(self, aIni, aEnd):
        try:
            self.list = []
            if self.fileName:
                with open(self.fileName, "r") as f:
                    vFile = f.readlines()
                    vFile = vFile[aIni:aEnd]
                    for line in vFile:
                        self.list.append(line.strip().replace('"', ''))
            self.EOF = bool(self.list)
        except:
            pass
            # print('s2')

    def getValue(self, aIndex):
        return self.list[aIndex]

    def next(self):
        try:
            if not self.list or not self.position <= len(self.list):
                self.load()
                self.position = -1
            if self.list:
                self.position += 1
                self.EOF = bool((self.position == len(self.list)))
                item = self.list[self.position]
                return item
        except:
            pass
            # print('CnpjManager: Index out of range')
