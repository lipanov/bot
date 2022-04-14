from typing import List
from qa_recognition.qa import Answer, QAPair, get_tags_by_text
from qa_recognition.jakkards_coefficent import calculate_jakkards_coefficent, calculate_strings_jakkards_coefficent
from qa_recognition.answer_recognizers import AnswerRecognizer


class BAlgorithmAnswerRecognizer(AnswerRecognizer):
    KEY = "B_Algorithm"

    def MIN_SIMILAR_TAGS_COUNT(self) -> int:
        return 2

    def MIN_TAG_SIMILARITY(self) -> float:
        return 0.69

    def recognize_answers(self, question: str, qa_pairs: List[QAPair]) -> List[Answer]:
        target_tags = get_tags_by_text(question)
        answers = []
        last_similar_tags_count = self.MIN_SIMILAR_TAGS_COUNT()

        for qa_pair in qa_pairs:
            question_tags = qa_pair.getTags()
            similar_tags_count = 0

            for target_tag in target_tags:
                for question_tag in question_tags:
                    if len(target_tag) > 1 and len(question_tag) > 1:
                        if calculate_strings_jakkards_coefficent(target_tag, question_tag) > self.MIN_TAG_SIMILARITY():
                            similar_tags_count += 1

            if similar_tags_count >= last_similar_tags_count:
                coefficent = calculate_jakkards_coefficent(len(target_tags), len(question_tags), similar_tags_count)
                answers.append(Answer(qa_pair, BAlgorithmAnswerRecognizer.KEY, coefficent))
                last_similar_tags_count = similar_tags_count

        answers.reverse()
        return answers
