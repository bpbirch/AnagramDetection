#%%
# some anagram detection stuff
# %%
import time
import matplotlib.pyplot as plt 
import matplotlib 
import numpy as np
import pandas as pd 
import math 
from itertools import permutations
import pickle 

# %%
# let's write some different algos for anagram detection
# anagram: checkoff
def checkOff(s1, s2):
    """    
    converts s2 to a list
    checks each character in s1 to see if it exists in s2. if so, entry in s2 is converted to None
    so i=1 checks n, i=2 checks n-1, so this runs as sum(i=1 to n)


    Args:
        s1 ([string]): [string]
        s2 ([string]): [gets converted to list]

    Returns:
        [Bool]: [tells us whether the two strings are anagrams or not]
    """
    start = time.time()
    if len(s1) != len(s2):
        end = time.time()
        return False, end-start
    l2 = list(s2)
    pos1 = 0
    stillOK = True

    while pos1 < len(s1) and stillOK:
        pos2 = 0
        found = False # here is our checker flag - reset to false each iteration through l2
        while pos2 < len(l2) and not found:
            if s1[pos1] == l2[pos2]:
                found = True # so this tells us to iterate through our outer while loop
            else:
                pos2 += 1 # if not found at current index, move to next one
        if found:
            l2[pos2] = None 
        else:
            stillOK = False # this is our signal to exit our outer while loop
        pos1 += 1

    end = time.time()
    return stillOK, end-start

if __name__ == '__main__':
    print(checkOff('ether', 'there')) # True, runtime
    print(checkOff('hello', 'there')) # False, runtime


# %%
# anagram: sorting and comparing
def sortedAnagram(s1, s2):
    """
    Sorts and then compares two strings to see if they're anagrams

    Args:
        s1 (string): string to be compared for anagram match
        s2 (string): string to be compared for anagram match

    Returns:
        stillOK, end-start (tuple): [(bool, time)]
    """

    start = time.time()
    if len(s1) != len(s2):
        end = time.time()
        return False, end-start
    sortedS1 = sorted(s1)
    sortedS2 = sorted(s2)
    pos = 0
    stillOK = True
    while pos < len(sortedS1) and stillOK:
        if sortedS1[pos] == sortedS2[pos]:
            pos += 1
        else:
            stillOK = False 
    end = time.time()
    return stillOK, end-start 

if __name__ == '__main__':
    print(sortedAnagram('ether', 'there')) # True, runtime
    print(sortedAnagram('hello', 'there')) # False, runtime
# %%
# anagram: count and compare
# in this approach we exploit the fact that the character count for each string will be identical

def countCompareAnagram(s1, s2):
    """
    this function creates a dictionary for s1 and s2, where the key:value
    pairs are composed of char:charCount for each char in each respective string

    Args:
        s1 (str): string to be compred to s2
        s2 (str): string to be compared to s1

    Returns:
        True/False, end-start (tuple): tuple of (pass/fail Bool, runtime)
    """
    start = time.time()
    if len(s1) != len(s2):
        end = time.time()
        return False, end - start 
    s1D = createCharDict(s1)
    s2D = createCharDict(s2)
    if s1D == s2D:
        end = time.time()
        return True, end-start
    else:
        end = time.time()
        return False, end-start


if __name__ == '__main__':
    print(countCompareAnagram('ether', 'there')) # True, runtime
    print(countCompareAnagram('hello', 'there')) # False, runtime

# %%
# defining createCharDict for use in countCompareAnagram
def createCharDict(word):
    """
    this function will create a dictionary out of the chars in word
    The key:value pairs in this dictionary will be char:charCount format

    Args:
        word (str): Word for which we wish to create a dictionary of char:charCount key:value pairs

    Returns:
        d (dict): dictionary of char:charCount key:value pairs for each char in word
    """
    d = {}
    for char in word:
        if char not in d:
            d[char] = 1
        else:
            d[char] += 1
    return d  

if __name__ == '__main__':
    pd = createCharDict('party')
    print(pd)
# %%
# let's write a function that can compare sorting algorithms
def anagramAnalysis(n, word, *funcs):
    """
    This function will create plots of runtime vs word length, for determining
    if two words are anagrams. It does so by taking one word as an argument,
    and permuting that word. The function concatenates the original string (s1)
    with itself n times, and the second string (s2) with permutations of itself n times,
    for each function. The function them plots time vs word length on a single plot
    using matplotlib.pyplot

    Args:
        n (int): how many times you want each function to run. Also
        how many times you want 'word' to be concatenated with itself

        word (str): string that is taken in. word will be compared with 
        permutations of itself in anagram analysis. 
    """
    funcNamesTimesLengths = []
    # the above list will contain tuples of (funcName, functimes, wordlengths)
    for func in funcs:
        s1 = s2 = word
        wordPerm = word
        lengths = []
        times = []
        for _ in range(n):
            result = func(s1, s2)
            lengths.append(len(s1))
            times.append(result[1])
            perms = list(permutations(word))
            randomNum = np.random.randint(0, len(perms))
            wordPerm = ''.join(perms[randomNum])
            s1 += word
            s2 += wordPerm
        funcNamesTimesLengths.append((func.__name__, times, lengths))

    ax = plt.subplot(111, xlabel='wordLength', ylabel='time')
    for (func, funcTimes, wordLengths) in funcNamesTimesLengths:
        ax.plot(wordLengths, funcTimes, label=func)
    plt.legend()
    plt.show()

if __name__ == '__main__':
    anagramAnalysis(50, 'hello', checkOff, sortedAnagram, countCompareAnagram)
    # our plot shows that sortedAnagram is O(1)
    # we also see that countCompareAnagram is O(1)

# %%
