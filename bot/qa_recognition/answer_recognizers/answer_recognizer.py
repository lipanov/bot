from typing import List
from qa_recognition.qa import Answer, QAPair


class AnswerRecognizer:
    def recognize_answers(question: str, qa_pairs: List[QAPair]) -> List[Answer]:
        pass
