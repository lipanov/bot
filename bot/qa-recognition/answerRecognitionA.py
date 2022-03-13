# Распознавание по схожим наборам букв, с использованием коэффицента Жаккара.

from typing import List
from qa import Answer, Question
from jakkardsCoefficent import calculateStringsJakkardsCoefficent


def MIN_ANSWER_CHANCE() -> float:
    return 0.6


def recognizeAnswers(questionText : str, questions : List[Question]) -> List[Answer]:
    answers = []
    lastAnswerChance = MIN_ANSWER_CHANCE()

    for q in questions:
        for qT in q.questionTexts:
            coefficent = calculateStringsJakkardsCoefficent(questionText, qT)
            if coefficent > lastAnswerChance:
                answers.append(Answer(q.answerText, coefficent))
                lastAnswerChance = coefficent

    return answers