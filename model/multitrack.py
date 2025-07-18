from steps_model import StepsLibrary, Step
from track import Track
from settings import TYPES_OF_STEP, JSON_KEYS

from typing import List, Optional, Dict, Any

class MultiTrack:
    def __init__(self, tracks_names:List[str]=None, tracks:List[Track]=None):
        self.tracks_names = tracks_names
        self.tracks = tracks