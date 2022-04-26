from typing import List
from qa_recognition.qa import Answer, QAPair, split_by_words
from qa_recognition.jakkards_coefficent import calculate_jakkards_coefficent, calculate_strings_jakkards_coefficent
from qa_recognition.answer_recognizers import AnswerRecognizer


class CAlgorithmAnswerRecognizer(AnswerRecognizer):
    KEY = "C_Algorithm"
    MIN_TAG_SIMILARITY = 0.6
    MIN_ANSWER_PROBABILITY = 0.5

    def recognize_answers(self, question: str, qa_pairs: List[QAPair]) -> List[Answer]:
        target_words = split_by_words(question)
        answers = []
        last_similarity = self.MIN_ANSWER_PROBABILITY

        for qa_pair in qa_pairs:
            question_words = qa_pair.get_words()
            similar_words_count = 0

            for target_word in target_words:
                for question_word in question_words:
                    if len(target_word) > 1 and len(question_word) > 1:
                        if calculate_strings_jakkards_coefficent(target_word.lower(), question_word.lower()) > self.MIN_TAG_SIMILARITY:
                            similar_words_count += 1

            coefficent = calculate_jakkards_coefficent(len(target_words), len(question_words), similar_words_count)

            if coefficent > last_similarity:
                answers.append(Answer(qa_pair, self.KEY, coefficent))
                last_similarity = coefficent

        answers.reverse()
        return answers
