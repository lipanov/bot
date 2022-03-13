from typing import List


def getTagsByText(text : str) -> List[str]:
    formatted = text
    formatted = formatted.replace("?", " ")
    formatted = formatted.replace(",", " ")
    formatted = formatted.replace(".", " ")
    formatted = formatted.replace("!", " ")
    return formatted.split()


class Question:
    questionTexts : List[str]
    answerText : str


    def __init__(self, questionTexts : List[str], answerText : str) -> None:
        lowered = []
        for question in questionTexts:
            lowered .append(question.lower())
        self.questionTexts = lowered
        self.answerText = answerText


    def getTags(self) -> List[str]:
        tags = []
        for q in self.questionTexts:
            tags += getTagsByText(q)
        return tags


class Answer:
    answerText : str
    chance : float


    def __init__(self, answer : str, chance : float) -> None:
        self.answerText = answer
        self.chance = chance


    def toString(self) -> str:
        return "// " + self.answerText + " : " + str(self.chance)