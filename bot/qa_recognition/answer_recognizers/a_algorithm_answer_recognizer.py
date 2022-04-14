from typing import List
from qa_recognition.qa import Answer, QAPair
from qa_recognition.jakkards_coefficent import calculate_strings_jakkards_coefficent
from qa_recognition.answer_recognizers import AnswerRecognizer


class AAlgorithmAnswerRecognizer(AnswerRecognizer):
    KEY = "A_Algorithm"

    def get_key(self) -> str:
        return "A_Algorithm"

    def MIN_ANSWER_CHANCE(self) -> float:
        return 0.5

    def recognize_answers(self, question: str, qa_pairs: List[QAPair]) -> List[Answer]:
        answers = []
        last_answer_chance = self.MIN_ANSWER_CHANCE()

        for qa_pair in qa_pairs:
            coefficent = calculate_strings_jakkards_coefficent(question.lower(), qa_pair.question.lower())
            if coefficent > last_answer_chance:
                answers.append(Answer(qa_pair, AAlgorithmAnswerRecognizer.KEY, coefficent))
                last_answer_chance = coefficent

        answers.reverse()
        return answers
