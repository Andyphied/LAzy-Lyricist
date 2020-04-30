from random import choice
from pymarkovchain import MarkovChain


def engine(lyrics, lines):
    mc = MarkovChain()
    
    mc.generateDatabase(lyrics)
    result = []
    for line in range(0, lines):
        result.append(mc.generateString())
    return result

    
