from typing import List
import re


def split_by_words(text: str) -> List[str]:
    formatted = text.lower()
    formatted = ''.join(re.findall(r'[a-zA-Zа-яА-Я ]', formatted))
    return list(set(formatted.split()))


class QAPair:
    id: int
    question: str
    answer: str
    tags: List[str]

    def __init__(self, id: int, question: str, answer: str, tags: List[str] = []) -> None:
        self.id = id
        self.question = question
        self.answer = answer
        self.tags = tags

    def get_words(self) -> List[str]:
        return split_by_words(self.question)

    def __str__(self):
        return self.question[:20] + "   " + self.answer[:20]


class Answer:
    qa_pair: QAPair
    algorithm_key: str
    probability: float

    def __init__(self, qa_pair: QAPair, algorithm_key: str, chance: float) -> None:
        self.qa_pair = qa_pair
        self.algorithm_key = algorithm_key
        self.probability = chance

    def __str__(self):
        return self.qa_pair[:20] + "   " + self.algorithm_key[:20]
