from typing import List
from qa_recognition.qa import Answer, QAPair, split_by_words
from qa_recognition.jakkards_coefficent import calculate_jakkards_coefficent, calculate_strings_jakkards_coefficent
from qa_recognition.answer_recognizers import AnswerRecognizer


class BAlgorithmAnswerRecognizer(AnswerRecognizer):
    KEY = "B_Algorithm"
    MIN_SIMILAR_TAGS_COUNT = 2
    MIN_TAG_SIMILARITY = 0.6

    def recognize_answers(self, question: str, qa_pairs: List[QAPair]) -> List[Answer]:
        target_words = split_by_words(question)
        answers = []
        last_similar_words_count = self.MIN_SIMILAR_TAGS_COUNT

        for qa_pair in qa_pairs:
            question_words = qa_pair.get_words()
            similar_words_count = 0

            for target_word in target_words:
                for question_word in question_words:
                    if len(target_word) > 1 and len(question_word) > 1:
                        if calculate_strings_jakkards_coefficent(target_word.lower(), question_word.lower()) > self.MIN_TAG_SIMILARITY:
                            similar_words_count += 1

            if similar_words_count >= last_similar_words_count:
                probability = calculate_jakkards_coefficent(len(target_words), len(question_words), similar_words_count)
                answers.append(Answer(qa_pair, self.KEY, probability))
                last_similar_words_count = similar_words_count

        answers.reverse()
        return answers
