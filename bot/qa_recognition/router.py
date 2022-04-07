from typing import Dict, List

from qa_recognition.qa import QAPair, Answer
from qa_recognition.answer_recognizers import AnswerRecognizer
from qa_recognition.answer_recognizers import AAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import BAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import CAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import DAlgorithmAnswerRecognizer

from DAO import SessionLogDAO


async def load_ratings() -> Dict[str, int]:
    session_log_DAO = SessionLogDAO()
    ratings = {}
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


async def get_recognizers() -> List[AnswerRecognizer]:
    recognizers = []

    recognizers.append(AAlgorithmAnswerRecognizer())
    recognizers.append(BAlgorithmAnswerRecognizer())
    recognizers.append(CAlgorithmAnswerRecognizer())
    recognizers.append(DAlgorithmAnswerRecognizer())

    ratings = await load_ratings()

    for key in ratings:
        for recognizer in recognizers:
            if recognizer.get_key() == key:
                recognizer.weight = ratings[key]

    return recognizers


async def get_most_relevant_answer(question: str, qa_pairs: List[QAPair]) -> Answer:
    recognizers = await get_recognizers()
    recognizers.sort(key=lambda r: r.weight, reverse=True)

    for recognizer in recognizers:
        answers = recognizer.recognize_answers(question, qa_pairs)

        if len(answers) > 0:
            return answers[0]

    return None
