from html.parser import HTMLParser

def removeValuesList(alist, avalues):
    for value in avalues:
        while value in alist:
            alist.remove(value)


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attrs):
        # print("Encountered a start tag:", tag)
        if tag != 'table':
            return
        if self.recording:
            self.recording += 1
            return
        for name, value in attrs:
            # print('tag: ', tag)
            if name == 'id' and value == 'Grid':
                break
        else:
            return

        self.recording = 1
        # for key, value in attrs:
        #     if((value == 'Grid') and (key == 'id')):
        #         print("     attr:", tag)

    def handle_endtag(self, tag):
        if tag == 'table' and self.recording:
            self.recording -= 1

    # def handle_startendtag(self, tag, attrs):
    #     print(tag)

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)

    def __del__(self):
        pass