
from HoloAI import HoloEcho
import logging

logger = logging.getLogger(__name__)

COMMANDS = {
    'voice': [
        "switch to voice", "voice mode", "enable voice", "listen to me", "activate voice"],
    'keyboard': [
        "switch to keyboard", "keyboard mode", "type mode", "disable voice", "back to typing"],
    'standby': [
        "standby", "stand by", "go to sleep", "wait mode", "stop listening"],
    'deactivate': [
        "deactivate", "shutdown", "turn off", "power down", "sleep mode", "go offline", "go dark"],
    'pause': [
        "pause", "hold on", "wait", "wait a minute"],
    'resume': [
        "resume", "continue", "carry on", "ok continue"],
    'stop': [
        "stop", "halt", "end", "cancel"]
}


class HoloVoice:
    def __init__(self, userName, assistantName, assistantGender, defaultMode):
        self.holoEcho        = HoloEcho()
        self.userName        = userName
        self.assistantName   = assistantName
        self.assistantGender = assistantGender
        self.defaultMode     = defaultMode
        self.soundChoice     = 1
        self.configVoice()

    def configVoice(self):
        self.holoEcho.setProperty("gender", self.assistantGender)
        self.holoEcho.setProperty("rate", 180)  # Speed of speech
        self.holoEcho.setProperty("pitch", 150) # Pitch of speech
        self.holoEcho.setProperty("volume", 1.0) # Volume level (0.0 to 1.0)
        self.holoEcho.setProperty("synthesisMode", 'advanced') # 'standard' or 'advanced'
        # Use listVoices() method to see available voices for standard voices
        self.holoEcho.setProperty("standardMaleVoice", 0)
        self.holoEcho.setProperty("standardFemaleVoice", 1)
        # Advanced Voices may take some time to load depending on your system due to downloading the model once downloaded it will be cached for future use
        self.holoEcho.setProperty("advancedMaleVoice", 11)
        self.holoEcho.setProperty("advancedFemaleVoice", 14)
        self.holoEcho.setProperty("mode", self.defaultMode)
        self.holoEcho.setProperty("commands", COMMANDS)

    def recognize(self) -> str:
        ambient = self._ambientInput()
        if ambient:
            return ambient
        option = self.holoEcho.mode.lower()
        optionMap = {
            'voice': self._voiceInput,
            'keyboard': self._keyboardInput
        }
        if option in optionMap:
            self.holoEcho.mode = option
            return optionMap[option]()
        raise ValueError("Invalid option. Use 'voice' or 'keyboard'.")

    def synthesize(self, text: str):
        if not text:
            return
        try:
            self._printMessage('assistant', text)
            self.holoEcho.synthesize(text, useThread=True) # can use threading if needed fir non-blocking behavior
        except Exception as e:
            logger.error(f"Error synthesizing text: {e}")
            print(f"Error synthesizing text: {e}")

    def parseCommands(self, command):
        self.holoEcho.parseCommands(command)

    def _voiceInput(self) -> str:
        self._printMessage('assistant', "is listening for input...")
        if self.holoEcho.isActivated:
            self.holoEcho.getSound(self.soundChoice)
        msg = self.holoEcho.voiceInput()
        if self.holoEcho.processing:
            self._printMessage('assistant', "processing...")
            self.holoEcho.processing = False
        if not msg:
            return None

        msg = msg.strip()

        if not self.holoEcho.isActivated:
            if self.assistantName.lower() in msg:
                self.holoEcho.isActivated = True
                printMsg = self.holoEcho.transcribeContext(msg)
                self._printMessage('user', printMsg)
                return msg
            return None
        printMsg = self.holoEcho.transcribeContext(msg)
        self._printMessage('user', printMsg)
        return msg

    def _ambientInput(self) -> str:
        return self.holoEcho.ambientInput()

    def _keyboardInput(self) -> str:
        msg = self.holoEcho.keyboardInput('Enter your input:\n')
        self._printMessage('user', msg)
        return msg.strip() if msg else None

    def _printMessage(self, type, text):
        self.holoEcho.streamMessage(type, text, name=self.assistantName)

    def listVoices(self):
        """
        List available voices for pyttsx4
        you can also install additional voices on your system
        and then list them to get their number IDs to use
        """
        self.holoEcho.listVoices()
