from typing import List


def get_tags_by_text(text: str) -> List[str]:
    formatted = text
    formatted = formatted.replace("?", " ")
    formatted = formatted.replace(",", " ")
    formatted = formatted.replace(".", " ")
    formatted = formatted.replace("!", " ")
    return formatted.split()


class QAPair:
    question: str
    answer: str

    def __init__(self, question: str, answer: str) -> None:
        self.question = question.lower()
        self.answer = answer

    def getTags(self) -> List[str]:
        return get_tags_by_text(self.question)


class Answer:
    answer_text: str
    algorithm_key: str
    probability: float

    def __init__(self, answer: str, algorithm_key: str, chance: float) -> None:
        self.answer_text = answer
        self.algorithm_key = algorithm_key
        self.probability = chance
