"""
This module contains the Config class for storing config data.
You can save and load config data to and from a json file.
Add new config data to the Config class and it will be able to save and load.

Example:
    Get the config data:
        >>> from src.config.config import config
        >>> buildArea = config.buildArea
        >>> unit = config.unit

    Modify the config class:
        class Config:
            buildArea: Box = Box((0, 0, 0), (255, 255, 255))
            unit: int = 2

            # You can add new config data here:
            dataStructuresPath: Path = Path("data/structures")

    Save the config data:
        >>> config.save("custom_config.json")

    Load the custom config data:
        >>> config = Config.load("custom_config.json")
"""

import json
from dataclasses import dataclass
from pathlib import Path
from gdpc.interface import DEFAULT_HOST
from gdpc.vector_tools import Box
from .generic_json import GenericJSONEncoder, GenericJSONDecoder

DEFAULT_CONFIG_PATH = Path("JEB_GEN_/config.json")


@dataclass
class Config:
    """Config class for storing config data"""

    def save(self, path: Path = DEFAULT_CONFIG_PATH):
        """Save config to a json file"""
        if not path.parent.exists():
            path.parent.mkdir(parents=True)
        with path.open("w") as f:
            json.dump(self, f, indent=4, cls=GenericJSONEncoder)

    @staticmethod
    def load(path: Path = DEFAULT_CONFIG_PATH) -> "Config":
        """Load config from a json file"""
        if not path.exists():
            return Config()
        with path.open("r") as f:
            data: Config = json.load(f, cls=GenericJSONDecoder)
            return data

    # ================ editor ================

    host: str = DEFAULT_HOST
    """The host of the editor"""

    buffering: bool = True
    """The buffering of the editor"""

    bufferLimit: int = 512
    """The buffer limit of the editor"""

    caching: bool = True
    """The caching of the editor"""

    doBlockUpdates: bool = False
    """Do block updates"""

    # ================ core ================

    buildArea: Box = Box((0, 0, 0), (255, 255, 255))
    """The area where buildings can be built"""

    unit: int = 2
    """The size of a single unit on the blueprint"""

    # ================ agent ================

    buildAgentCooldown: int = 2
    """The cooldown of the build agent"""

    roadAgentCooldown: int = 0
    """The cooldown of the road agent"""

    numBasicAgents: int = 3
    """The number of basic agents"""

    numSpecialAgents: int = 1
    """The number of special agents"""

    sampleRate: float = 0.25
    """The sample rate of locations to analyze for agents"""

    maxSampleTimes: int = 15000
    """The maximum sample times of locations to analyze for agents"""

    noSuitableLocationPenalty: int = 1000000
    """The penalty of no suitable location"""

    # ================ analyzer ================

    analyzeBorder: int = 2

    flatnessThreshold: float = 0.4

    desertnessThreshold: float = 0.4

    forestThreshold: float = 4/(16*16)
    """"4 leaves per chunk"""

    forestQueryMargin: int = 16

    rockThreshold: float = 0.1/(16*16)
    """"0.1 rock per chunk"""

    rockQueryMargin: int = 16

    minimumBuildingMargin: int = 256

    minimumBoundPadding = 10

    # ================ data ================

    structuresPath: Path = Path("JEB_GEN_/data/structures")
    """The path to the data of structures"""

    levelLimitPath: Path = Path("JEB_GEN_/data/level_limit/limit.json")
    """The path to the data of level"""

    # ================ road ================

    roadMaterial: str = "minecraft:dirt_path"
    """The material of the road"""

    # ================ main ================
    gameRound: int = 150

config = Config.load()
