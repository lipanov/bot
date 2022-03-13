# Распознавание по определенному количеству схожих тегов, с использование коэффицента Жаккара.
# Допускается определнный процент ошибок в тегах.

from ctypes.wintypes import tagSIZE
from typing import List
from qa import *
from jakkardsCoefficent import calculateJakkardsCoefficent, calculateStringsJakkardsCoefficent


def MIN_SIMILAR_TAGS_COUNT() -> int:
    return 1


def MIN_TAG_SIMILARITY() -> float:
    return 0.6


def recognizeAnswers(questionText : str, questions : List[Question]) -> List[Answer]:
    targetTags = getTagsByText(questionText)
    answers = []
    lastSimilarTagsCount = MIN_SIMILAR_TAGS_COUNT()

    for q in questions:
        qTags = q.getTags()
        similarTagsCount = 0

        for targetTag in targetTags:
            for qTag in qTags:
                if calculateStringsJakkardsCoefficent(targetTag, qTag) > MIN_TAG_SIMILARITY():
                    similarTagsCount += 1
        
        if similarTagsCount >= lastSimilarTagsCount:
            coefficent = calculateJakkardsCoefficent(len(targetTags), len(qTags), similarTagsCount)
            answers.append(Answer(q.answerText, coefficent))
            lastSimilarTagsCount = similarTagsCount

    return answers