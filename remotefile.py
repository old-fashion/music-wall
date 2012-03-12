import re
import httplib
import os

class RemoteFile(object):
    TIMEOUT = 10
    URLPARSER = re.compile(r"^(http://|https://)(?P<host>[^/]*)/(?P<file>.*)")

    def __init__(self, url):
        self.valid = False
        self.url = url
        m = self.URLPARSER.search(url)
        self.host = m.group('host')
        self.file = "/" + m.group('file')
        self.size = 0
        self.currpos = 0
        self.headers = {}
        self.log = []

        self.conn = httplib.HTTPConnection(self.host, timeout=self.TIMEOUT)
        headers = {'Connection': 'keep-alive'}
        self.conn.request("HEAD", self.file, headers=headers)
        result = self.conn.getresponse()
        self.reason = result.reason
        if result.status == 200:
            self.valid = True
            self.size = int(result.getheader('content-length', '0'))
            self.headers = result.getheaders()

    def read(self, size):
        if not self.valid:
            return
        self.conn = httplib.HTTPConnection(self.host, timeout=self.TIMEOUT)
        headers = { 'Connection': 'keep-alive',
                   'Range': "bytes={}-{}".format(self.currpos, \
                                    min(self.currpos + size - 1, self.size-1))}
        self.conn.request("GET", self.file, headers=headers)
        result = self.conn.getresponse()
        self.log.append("READ    pos={}, size={}".format(self.currpos, size))
        self.currpos += size

        return result.read()

    def seek(self, offset, whence=os.SEEK_SET):
        if whence == os.SEEK_SET:
            self.currpos = offset
        elif whence == os.SEEK_CUR:
            self.curpos += offset
        elif whence == os.SEEK_END:
            self.curpos = self.size + offset
        self.log.append("SEEK    pos={}, size={}, whence={}".format(self.currpos, offset, whence))

    def tell(self):
        return self.currpos

    def close(self):
        #print self.pprint()
        pass

    def pprint(self):
        result = ""
        result += "host = {}\n".format(self.host)
        result += "file = {}\n".format(self.file)
        result += "size = {}\n".format(self.size)
        result += "currpos = {}\n".format(self.currpos)
        result += "headers = {}\n".format(self.headers)
        result += "valid = {}\n".format(self.valid)
        result += "reason = {}\n".format(self.reason)
        result += "log =\n"
        for log in self.log:
            result += "  {}\n".format(log)
        return result

if __name__ == "__main__":
    #rf = RemoteFile("http://blackout.lgnas.com:9000/1.mp3")
    rf = RemoteFile("http://blackout.lgnas.com:9000/disk/volume1/Multimedia/Music/OST/Vicky%20Cristina%20Barcelona%20%282008%29/01%20Barcelona.mp3")
    print rf.pprint()

    data = rf.read(10)
    print data, data.encode("hex"), len(data)
    rf.seek(10)
    print rf.read(10)
    print rf.pprint()
    #remotetag.extract("file://1.mp3")

