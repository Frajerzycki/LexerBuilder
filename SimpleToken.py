
class SimpleToken():
    text = ""
    type = ""
    def get_type(self):
        return self.type
    def __init__(self,type):
        self.type = type
    def set_text(self,text):
        self.text = text
    def get_text(self):
        return self.text
