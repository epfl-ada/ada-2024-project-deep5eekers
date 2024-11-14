from src.booknlp.character import CharacterDataset, GENDER_DICT
from pathlib import Path
from collections import defaultdict, Counter
from functools import cached_property
import pandas as pd

import nltk
nltk.download('wordnet')

from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

class EventDataset(CharacterDataset):
    """
    A dataset class to analyze events associated with characters by gender.
    Events are categorized into agent, patient, and possessor roles.
    """
    
    def __init__(self, dir: Path):
        """
        Initializes the EventDataset, building event lists for each character
        categorized by gender.
        
        Parameters:
            dir (Path): The directory path to the dataset files.
        """
        super().__init__(dir)
        self.lemmatizer = WordNetLemmatizer()
        self.agent_events = defaultdict(list)
        self.patient_events = defaultdict(list)
        self.poss_events = defaultdict(list)
        self._build()

    def _preprocess_verbs(self, verbs):
        """
        Preprocesses a list of verbs by converting to lowercase, lemmatizing, and counting frequencies.
        """
        verbs = [self.lemmatizer.lemmatize(verb.lower(), wordnet.VERB) for verb in verbs]
        return Counter(verbs)

    def _build(self):
        """
        Builds the event datasets by collecting verbs from each character's actions
        categorized as agent, patient, or possessor, and processes them by gender.
        """
        # Collect verbs by gender
        for ch in self.characters:
            self.agent_events[ch.gender].extend(ch.agent_word)
            self.patient_events[ch.gender].extend(ch.patient_word)
            self.poss_events[ch.gender].extend(ch.poss_word)

        # Process verbs for each gender category
        for gender in GENDER_DICT.values():
            self.agent_events[gender] = self._preprocess_verbs(self.agent_events[gender])
            self.patient_events[gender] = self._preprocess_verbs(self.patient_events[gender])
            self.poss_events[gender] = self._preprocess_verbs(self.poss_events[gender])
