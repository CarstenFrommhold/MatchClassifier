from typing import List, Dict
import fuzzywuzzy.fuzz
import numpy as np


def map_names(from_: List[str], to: List[str]) -> Dict:
    """ Simple mapping helper
    Allocate each entry in from_ to the "nearest" entry in to
    """
    map = {}
    for entry_from in from_:
        ratios = [fuzzywuzzy.fuzz.ratio(entry_from, entry_to) for entry_to in to]
        map[entry_from] = to[np.argmax(ratios)]
    return map

