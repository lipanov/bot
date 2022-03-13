# Распознавание по количеству схожих тегов и их проценту от общего числа тегов (в приоритете количество),
# с использованием коэффицента Жаккара.
# Допускается определнный процент ошибок в тегах.

from typing import List
from jakkardsCoefficent import calculateJakkardsCoefficent
from jakkardsCoefficent import calculateStringsJakkardsCoefficent
from qa import *


def MIN_SIMILAR_TAGS_COUNT() -> int:
    return 1


def MIN_TAG_SIMILARITY() -> float:
    return 0.5
    

def MIN_ANSWER_SIMILARITY() -> float:
    return 0.7


def recognizeAnswers(questionText : str, questions : List[Question]) -> List[Answer]:
    targetTags = getTagsByText(questionText)
    answers = []
    lastSimilarity = MIN_ANSWER_SIMILARITY()
    lastSimilarTagsCount = MIN_SIMILAR_TAGS_COUNT()

    for q in questions:
        qTags = q.getTags()
        similarTagsCount = 0

        for targetTag in targetTags:
            for qTag in qTags:
                if calculateStringsJakkardsCoefficent(targetTag, qTag) > MIN_TAG_SIMILARITY():
                    similarTagsCount += 1

        coefficent = calculateJakkardsCoefficent(len(targetTags), len(qTags), similarTagsCount)
        
        if similarTagsCount >= lastSimilarTagsCount:
            answers.append(Answer(q.answerText, coefficent))
            lastSimilarity = coefficent
            lastSimilarTagsCount = similarTagsCount

        if similarTagsCount == lastSimilarTagsCount:
            if coefficent > lastSimilarity:
                answers.append(Answer(q.answerText, coefficent))
                lastSimilarity = coefficent
                lastSimilarTagsCount = similarTagsCount

    return answers