from typing import Dict, List

from qa_recognition.qa import QAPair, Answer
from qa_recognition.answer_recognizers import AAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import BAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import CAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import DAlgorithmAnswerRecognizer

from qa_recognition.routers import Router

from DAO import SessionLogDAO


class RatingRouter(Router):
    recognizers = {
        AAlgorithmAnswerRecognizer.KEY: AAlgorithmAnswerRecognizer(),
        BAlgorithmAnswerRecognizer.KEY: BAlgorithmAnswerRecognizer(),
        CAlgorithmAnswerRecognizer.KEY: CAlgorithmAnswerRecognizer(),
        DAlgorithmAnswerRecognizer.KEY: DAlgorithmAnswerRecognizer()
    }

    async def get_most_relevant_answer(question: str, qa_pairs: List[QAPair]) -> Answer:
        answers = await RatingRouter.get_most_relevant_answers(question, qa_pairs)
        if len(answers) > 0:
            return answers[0]
        else:
            return None

    async def get_most_relevant_answers(question: str, qa_pairs: List[QAPair]) -> List[Answer]:
        algorithm_keys = await RatingRouter.get_algorithm_keys_sorted_by_rating()
        answers = []

        for key in algorithm_keys:
            answers = RatingRouter.recognizers[key].recognize_answers(question, qa_pairs)
            if len(answers) > 0:
                return answers

        return answers

    async def get_algorithm_keys_sorted_by_rating() -> List[str]:
        algorithm_keys = []
        ratings = await RatingRouter.load_ratings()
        sorted_rating_items = sorted(ratings.items(), key=lambda item: item[1], reverse=True)

        for item in sorted_rating_items:
            algorithm_keys.append(item[0])

        return algorithm_keys

    async def load_ratings() -> Dict[str, int]:
        session_log_DAO = SessionLogDAO()
        ratings = {}

        for key in RatingRouter.recognizers:
            ratings[key] = 0

        session_log_records = await session_log_DAO.get_many()

        if session_log_records != None:
            for session_log_record in session_log_records:
                session_log_record_dict = dict(session_log_record)

                if not(session_log_record_dict["SessionLog_algorithm"] in ratings):
                    ratings[session_log_record_dict["SessionLog_algorithm"]] = 0

                successful = bool(session_log_record_dict["SessionLog_successful"])

                if successful:
                    ratings[session_log_record_dict["SessionLog_algorithm"]] += 1
                else:
                    ratings[session_log_record_dict["SessionLog_algorithm"]] -= 1

        return ratings
