from typing import List


def getTagsByText(text : str) -> List[str]:
    formatted = text
    formatted = formatted.replace("?", " ")
    formatted = formatted.replace(",", " ")
    formatted = formatted.replace(".", " ")
    formatted = formatted.replace("!", " ")
    return formatted.split()


class QAPair:
    question : str
    answer : str

    def __init__(self, question : str, answer : str) -> None:
        self.question = question.lower()
        self.answer = answer


    def getTags(self) -> List[str]:
        return getTagsByText(self.question)


class Answer:
    answerText : str
    algorithm_key : str
    probability : float


    def __init__(self, answer : str, algorithm_key : str, chance : float) -> None:
        self.answerText = answer
        self.algorithm_key = algorithm_key
        self.probability = chance


    def toString(self) -> str:
        return "// " + self.answerText + " : " + str(self.probability)