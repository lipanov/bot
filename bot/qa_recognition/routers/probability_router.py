from typing import List

from qa_recognition.qa import QAPair, Answer
from qa_recognition.answer_recognizers import AAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import BAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import CAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import DAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import NetworkAnswerRecognizer

from qa_recognition.routers import Router


class ProbabilityRouter(Router):
    recognizers = {
        AAlgorithmAnswerRecognizer.KEY: AAlgorithmAnswerRecognizer(),
        BAlgorithmAnswerRecognizer.KEY: BAlgorithmAnswerRecognizer(),
        CAlgorithmAnswerRecognizer.KEY: CAlgorithmAnswerRecognizer(),
        DAlgorithmAnswerRecognizer.KEY: DAlgorithmAnswerRecognizer(),
        NetworkAnswerRecognizer.KEY: NetworkAnswerRecognizer()
    }

    async def get_most_relevant_answer(question: str, qa_pairs: List[QAPair]) -> Answer:
        answers = await ProbabilityRouter.get_most_relevant_answers(question, qa_pairs)
        if len(answers) > 0:
            return answers[0]
        else:
            return None

    async def get_most_relevant_answers(question: str, qa_pairs: List[QAPair]) -> List[Answer]:
        result_answers = []

        for key in ProbabilityRouter.recognizers:
            answers = ProbabilityRouter.recognizers[key].recognize_answers(question, qa_pairs)
            print(key, question, answers)
            for answer in answers:
                is_duplicate = False

                for appended_answer in result_answers:
                    if appended_answer.qa_pair == answer.qa_pair:
                        is_duplicate = True

                if is_duplicate == False:
                    result_answers.append(answer)

        return sorted(result_answers, key=lambda a: a.probability, reverse=True)
