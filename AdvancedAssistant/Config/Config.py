
import os
import sys
import time
from dotenv import load_dotenv
from datetime import datetime

from HoloAI import HoloAI
from Voice.Voice import HoloVoice
from Skills.Skills import Skills

load_dotenv()

# # Set These Environment Variables in your .env file or system environment variables for the provider(s) you want to use
# # PROVIDER=openai or google (default is openai)
# # OPENAI_API_KEY=your_openai_api_key
# # GOOGLE_API_KEY=your_google_api_key
# # GROQ_API_KEY=your_groq_api_key
# # ANTHROPIC_API_KEY=your_anthropic_api_key
# # XAI_API_KEY=your_xai_api_key

# #-------------------------------- NOTE --------------------------------
# # HoloAI supports OpenAI, Google, xAI, Anthropic, Groq.

# #----------------------- Provider Configuration -----------------------
# # You can set it directly like this instead of using an environment variable:
# # PROVIDER = "openai"  # or "google", "groq", "anthropic", "xai"

# Defaults
DEFAULTS = {
    "USER_NAME":        "Tristan McBride Sr.",
    "ASSISTANT_NAME":   "Alias",
    "ASSISTANT_GENDER": "Female",
    "DEFAULT_MODE":     "keyboard",
    "MAX_TURNS":        10
}

# Load from env with fallback to defaults
USER_NAME        = os.getenv("USER_NAME", DEFAULTS["USER_NAME"])
ASSISTANT_NAME   = os.getenv("ASSISTANT_NAME", DEFAULTS["ASSISTANT_NAME"])
ASSISTANT_GENDER = os.getenv("ASSISTANT_GENDER", DEFAULTS["ASSISTANT_GENDER"])
DEFAULT_MODE     = os.getenv("DEFAULT_MODE", DEFAULTS["DEFAULT_MODE"])
MAX_TURNS        = int(os.getenv("MAX_TURNS", DEFAULTS["MAX_TURNS"]))

class Config:
    def __init__(self):
        self.client    = HoloAI()
        self.holoVoice = HoloVoice(USER_NAME, ASSISTANT_NAME, ASSISTANT_GENDER, DEFAULT_MODE)
        self.skills    = Skills()
        self.provider  = os.getenv("PROVIDER", "openai").lower()
        self.providers = {
            # You can mix and match models from different providers as long as you have the API keys set
            "mixed": {
                "response": os.getenv("OPENAI_RESPONSE_MODEL", "gpt-4.1"),
                "vision": os.getenv("GEMINI_VISION_MODEL", "gemini-2.5-flash"),
                "generation": os.getenv("XAI_IMAGE_MODEL", "grok-2-image"),
            },
            "openai": {
                "response": os.getenv("OPENAI_RESPONSE_MODEL", "gpt-4.1"),
                "vision": os.getenv("OPENAI_VISION_MODEL", "gpt-4.1"),
                "generation": os.getenv("OPENAI_GENERATION_MODEL", "dall-e-3"),
            },
            "google": {
                "response": os.getenv("GEMINI_RESPONSE_MODEL", "gemini-2.5-flash"),
                "vision": os.getenv("GEMINI_VISION_MODEL", "gemini-2.5-flash"),
                "generation": os.getenv("GOOGLE_IMAGE_MODEL", "gemini-2.0-flash-preview-image-generation"),
            },
            "groq": {
                "response": os.getenv("GROQ_RESPONSE_MODEL", "llama-3.3-70b-versatile"),
                "vision": os.getenv("GROQ_VISION_MODEL", "meta-llama/llama-4-scout-17b-16e-instruct"),
                "generation": os.getenv("GROQ_IMAGE_MODEL", "grok-2-image"),
            },
            "anthropic": {
                "response": os.getenv("ANTHROPIC_RESPONSE_MODEL", "claude-3.5-sonnet"),
                "vision": os.getenv("ANTHROPIC_VISION_MODEL", "claude-3.5-sonnet"),
                "generation": os.getenv("ANTHROPIC_IMAGE_MODEL", "grok-2-image"),
            },
            "xai": {
                "response": os.getenv("XAI_RESPONSE_MODEL", "grok-4"),
                "vision": os.getenv("XAI_VISION_MODEL", "grok-4"),
                "generation": os.getenv("XAI_IMAGE_MODEL", "grok-2-image"),
            },
        }
        self.memories = []
        self.startMsg = False

    def HoloCompletion(self, user: str) -> str:
        skills  = self.skills.getAgentSkills()
        actions = self.skills.getAgentActions()
        system, instructions = self.systemInstructions()
        msgs = self.client.formatConversation(self.memories, user)

        models = self.getModels()

        resp = self.client.HoloAssist(
            models=[models["response"], models["vision"], models["generation"]],
            system=system,
            instructions=instructions,
            input=msgs,
            output=r".\CreatedImages",  # adjust for OS
            capabilities=[skills, actions],
            tokens=4096,
            creativity=0.2,
        )
        if resp:
            self.addMemory(user, resp)
        return resp

    def addMemory(self, user, response):
        self.memories.append(f"user:{user}")
        self.memories.append(f"assistant:{response}")
        if len(self.memories) > MAX_TURNS * 2:
            self.memories = self.memories[-MAX_TURNS * 2 :]

    def systemInstructions(self):
        system = f"You are {ASSISTANT_NAME}, a {ASSISTANT_GENDER} AI assistant. Be concise, clear, and professional."
        instructions = (
            f"The current user is {USER_NAME}.\n"
            f"The current date and time is {datetime.now().strftime('%B %d, %Y %I:%M %p')}."
        )
        return system, instructions

    def getModels(self):
        return self.providers.get(self.provider, self.providers["openai"])

    def setProvider(self, provider: str):
        if provider.lower() in self.providers:
            self.provider = provider.lower()
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def recognize(self):
        if not self.startMsg:
            text = (f"\nHello {USER_NAME}, I am {ASSISTANT_NAME} your Holo Assistant.\n I'm online and ready to assist you.\n")
            self.printStream(text, mode="word", delay=0.13)
            self.startMsg = True
        return self.holoVoice.recognize()

    def parseCommands(self, command):
        return self.holoVoice.parseCommands(command)

    def synthesize(self, text: str):
        self.holoVoice.synthesize(text)

    def printStream(self, text: str, mode: str = "char", delay: float = None):
        self.holoVoice.holoEcho.printStream(text, mode, delay)
