from typing import List
from qa_recognition.qa import Answer, QAPair
from qa_recognition.jakkards_coefficent import calculate_strings_jakkards_coefficent
from qa_recognition.answer_recognizers import AnswerRecognizer


class AAlgorithmAnswerRecognizer(AnswerRecognizer):
    KEY = "A_Algorithm"
    MIN_ANSWER_PROBABILITY = 0.7

    def recognize_answers(self, question: str, qa_pairs: List[QAPair]) -> List[Answer]:
        answers = []
        last_answer_probability = self.MIN_ANSWER_PROBABILITY

        for qa_pair in qa_pairs:
            probability = calculate_strings_jakkards_coefficent(question.lower(), qa_pair.question.lower())
            if probability > last_answer_probability:
                answers.append(Answer(qa_pair, self.KEY, probability))
                last_answer_probability = probability

        answers.reverse()
        return answers
