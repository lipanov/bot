from typing import List


def get_tags_by_text(text: str) -> List[str]:
    formatted = text
    formatted = formatted.replace("?", " ")
    formatted = formatted.replace(",", " ")
    formatted = formatted.replace(".", " ")
    formatted = formatted.replace("!", " ")
    return list(set(formatted.split()))


class QAPair:
    question: str
    answer: str

    def __init__(self, question: str, answer: str) -> None:
        self.question = question.lower()
        self.answer = answer

    def get_tags(self) -> List[str]:
        return get_tags_by_text(self.question)


class Answer:
    qa_pair: QAPair
    algorithm_key: str
    probability: float

    def __init__(self, qa_pair: QAPair, algorithm_key: str, chance: float) -> None:
        self.qa_pair = qa_pair
        self.algorithm_key = algorithm_key
        self.probability = chance
