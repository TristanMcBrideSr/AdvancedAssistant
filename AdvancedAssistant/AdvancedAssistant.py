
from Config.Config import Config


class HoloAssistant:
    def __init__(self):
        self.config = Config()

    def run(self):
        while True:
            userInput = self.config.recognize()
            if not userInput:
                continue
            if self.config.parseCommands(userInput):
                continue
            reply = self.config.HoloCompletion(userInput)
            if reply:
                self.config.synthesize(reply)
            else:
                print("No response from Holo Assistant, please try again.")


if __name__ == "__main__":
    HoloAssistant().run()
