log_pos = 'positive'
log_neutral = 'neutral'
log_neg = 'negative'

from gameHelper import printRedLine, printGreenLine

class Log():
    def __init__(self, text, log_type):
        self.text: str = text
        self.log_type: str = log_type

        self.log()

    def log(self):
        if self.log_type == log_pos:
            printGreenLine(self.text)
        elif self.log_type == log_neg:
            printRedLine(self.text)
        else:
            print(self.text)

    def toJson(self):
        resJson = {
            "log": self.text,
            "logType": self.log_type
        }

        return resJson
