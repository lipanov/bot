def getWordCharacterCountPairs(word):
    word = word.lower()
    characterCounts = {}

    for c in word:
        if c in characterCounts:
            characterCounts[c] += 1
        else:
            characterCounts[c] = 1

    return characterCounts

def getCharacterCountPairsIntersection(aCharacterCounts, bCharacterCounts):
    intersection = {}
    for character in aCharacterCounts:
        if character in bCharacterCounts:
            if not(character in intersection):
                if aCharacterCounts[character] > bCharacterCounts[character]:
                    intersection[character] = bCharacterCounts[character]
                else:
                    intersection[character] = aCharacterCounts[character]
    return intersection

def getCharacterCounts(characterCountPairs):
    count = 0
    for key in characterCountPairs:
        count += characterCountPairs[key]
    return count

def getWordsSimilarityCoefficent(wordA, wordB):
    wordACharacterCountPairs = getWordCharacterCountPairs(wordA)
    wordBCharacterCountPairs = getWordCharacterCountPairs(wordB)
    intersection = getCharacterCountPairsIntersection(wordACharacterCountPairs, wordBCharacterCountPairs)
    
    a = getCharacterCounts(wordACharacterCountPairs)
    b = getCharacterCounts(wordBCharacterCountPairs)
    c = getCharacterCounts(intersection)

    k = c / (a + b - c)
    return k
