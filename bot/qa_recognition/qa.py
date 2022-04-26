from typing import List


def split_by_words(text: str) -> List[str]:
    formatted = text
    formatted = formatted.replace("?", " ")
    formatted = formatted.replace(",", " ")
    formatted = formatted.replace(".", " ")
    formatted = formatted.replace("!", " ")
    return list(set(formatted.split()))


class QAPair:
    id: int
    question: str
    answer: str
    tags: List[str]

    def __init__(self, id: int, question: str, answer: str, tags: List[str] = []) -> None:
        self.id = id
        self.question = question.lower()
        self.answer = answer
        self.tags = tags

    def get_words(self) -> List[str]:
        return split_by_words(self.question)


class Answer:
    qa_pair: QAPair
    algorithm_key: str
    probability: float

    def __init__(self, qa_pair: QAPair, algorithm_key: str, chance: float) -> None:
        self.qa_pair = qa_pair
        self.algorithm_key = algorithm_key
        self.probability = chance
