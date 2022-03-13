# Распознавание по проценту схожих тегов, с использованием коэффицента Жаккара.
# Допускается определнный процент ошибок в тегах.

from typing import List
from jakkardsCoefficent import calculateJakkardsCoefficent
from jakkardsCoefficent import calculateStringsJakkardsCoefficent
from qa import *


def MIN_TAG_SIMILARITY():
    return 0.5


def MIN_ANSWER_SIMILARITY() -> float:
    return 0.6


def recognizeAnswers(questionText : str, questions : List[Question]) -> List[Answer]:
    targetTags = getTagsByText(questionText)
    answers = []
    lastSimilarity = MIN_ANSWER_SIMILARITY()

    for q in questions:
        qTags = q.getTags()
        similarTagsCount = 0

        for targetTag in targetTags:
            for qTag in qTags:
                if calculateStringsJakkardsCoefficent(targetTag, qTag) > MIN_TAG_SIMILARITY():
                    similarTagsCount += 1

        coefficent = calculateJakkardsCoefficent(len(targetTags), len(qTags), similarTagsCount)
        
        if coefficent >= lastSimilarity:
            answers.append(Answer(q.answerText, coefficent))
            lastSimilarity = coefficent

    return answers