
import json
import re
import inspect
import os
import threading
import logging
from dotenv import load_dotenv
from pathlib import Path
from google.genai import types
from HoloAI import HoloLink

load_dotenv()

logger = logging.getLogger(__name__)


class Skills:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(Skills, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if getattr(self, 'initialized', False):
            return
        self._initComponents()
        self.initialized = True

    def _initComponents(self):
        self.holoLink         = HoloLink()
        self.baseSkillsDir    = self.getDir('Skills')
        self.showCapabilities = os.getenv('SHOW_CAPABILITIES', 'False') == 'True'
        self.showMetaData     = os.getenv('SHOW_METADATA', 'False') == 'True'
        self.loadAllComponents()
        if self.showCapabilities:
            self.getAgentSkills()
        if self.showMetaData:
            self.getMetaData()

    def getDir(self, *paths):
        return self.holoLink.getDir(*paths)

    def loadAllComponents(self):
        """
        Load all components from the specified directories.
        This method loads skills and tools from the 'Skills' directory.
        It also loads custom tools for the agent.
        """
        self.userSkills  = []
        self.agentSkills = []

        self.holoLink.loadComponents(
            paths=[
                [self.getDir(self.baseSkillsDir, 'User')],
                [self.getDir(self.baseSkillsDir, 'Agent')],
            ],
            components=[
                self.userSkills,
                self.agentSkills,
            ],
            reloadable=[
                False,
                False,# This is for dynamic skills, so set to True if you want to reload them this will also set autoReload to True with a cycleInterval of 60 seconds.
                # False
            ],
            #cycleInterval=60 # Optional, set the cycle interval in seconds for auto reloading skills (default is 60 seconds).
        )

    def getUserActions(self, content):
        """
        Get user actions based on the provided content.
        This method combines dynamic, static, and restricted user skills to return the available actions.
        Use only if you want to get user actions based on the content provided.
        """
        skills = (
            self.userSkills
        )
        return self.holoLink.getComponents(skills, content)

    def getAgentActions(self):
        """
        Get self actions based on the skills available.
        This method combines dynamic, static, and restricted self skills.
        """
        skills = (
            self.agentSkills
        )
        return self.holoLink.getComponents(skills)

    def reloadSkills(self):
        """
        Reload all skills and print any new skills added.
        """
        original = self.getMetaData()
        self.holoLink.reloadSkills()
        new = self.getMetaData()
        for skill in new:
            if skill not in original:
                print(f"I've added the new skill {skill['className']} That {skill['description']}.\n")

    def getMetaData(self):
        """Get metadata for all skills."""
        metaData = (
                self.agentSkills
        )
        return self.holoLink.getMetaData(metaData, self.showMetaData)

    # ----- Skills -----
    def getAgentSkills(self):
        """
        Get the capabilities of the agent based on its skills.
        This method retrieves the capabilities of the agent's skills and returns them in a structured format.
        """
        description = False
        capabitites = (
            self.agentSkills
        )
        return self.holoLink.getCapabilities(capabitites, self.showCapabilities, description)

    def checkActions(self, action: str) -> str:
        """
        Check if the given action is valid based on the agent's skills.
        Returns a string indicating whether the action is valid or not.
        """
        return self.holoLink.actionParser.checkActions(action)

    def getActions(self, action: str) -> list:
        """
        Get a list of actions based on the given action string.
        This method uses the skills manager's action parser to retrieve actions that match the given string.
        If the action is not found, it returns an empty list.
        """
        return self.holoLink.actionParser.getActions(action)

    def executeAction(self, actions, action):
        """
        Execute a single action based on the provided actions and action string.
        You must create your own for loop if you want to execute multiple actions.
        """
        return self.holoLink.actionParser.executeAction(actions, action)

    def executeActions(self, actions, action):
        """
        Execute both single and multiple actions based on the provided actions and action string.
        The for loop is handled internally, so you can pass a single action or a list of actions.
        """
        return self.holoLink.actionParser.executeActions(actions, action)

    def skillInstructions(self):
        """
        Get skill instructions for the agent based on its capabilities.
        """
        return self.holoLink.skillInstructions(self.getAgentSkills())
