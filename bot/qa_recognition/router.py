from typing import Dict, List

from qa_recognition.qa import QAPair, Answer

from qa_recognition.answer_recognizers import AnswerRecognizer
from qa_recognition.answer_recognizers import AAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import BAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import CAlgorithmAnswerRecognizer
from qa_recognition.answer_recognizers import DAlgorithmAnswerRecognizer

from DAO import QuestionAnswerDAO, SessionLogDAO


async def load_qa_pairs() -> List[QAPair]:
    qaPairs = []
    questionsAnswers = QuestionAnswerDAO()
    records = await questionsAnswers.get_many()

    if records != None:
        for record in records:
            qaPair = dict(record)
            qaPairs.append(QAPair(qaPair["QuestionAnswer_question"], qaPair["QuestionAnswer_answer"]))

    return qaPairs


async def load_ratings() -> Dict[str, int]:
    sessionLogs = SessionLogDAO()
    ratings = {}
    records = await sessionLogs.get_many()

    if records != None:
        for record in records:
            sessionLog = dict(record)

            if not(sessionLog["SessionLog_algorithm"] in ratings):
                ratings[sessionLog["SessionLog_algorithm"]] = 0

            successful = bool(sessionLog["SessionLog_successful"])

            if successful:
                ratings[sessionLog["SessionLog_algorithm"]] += 1
            else:
                ratings[sessionLog["SessionLog_algorithm"]] -= 1

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


async def get_most_relevant_answer(question : str) -> Answer:
    qaPairs = await load_qa_pairs()
    recognizers = await get_recognizers()
    recognizers.sort(key=lambda r: r.weight, reverse=True)

    for recognizer in recognizers:
        answers = recognizer.recognize_answers(question, qaPairs)

        if len(answers) > 0:
            return answers[0]

    return None