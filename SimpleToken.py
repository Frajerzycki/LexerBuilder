
class SimpleToken():
    text = ""
    type = ""
    def get_type(self):
        return self.token
    def __init__(self,token):
        self.token = token
    def set_text(self,text):
        self.text = text
    def get_text(self):
        return self.text