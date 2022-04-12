from asyncpg import Record
from typing import List

from qa_recognition.qa import QAPair

from DAO import QuestionAnswerDAO, QuestionAnswerFlagDAO

GENERAL_QA_FLAG = 'Общие'

ENROLLEE_QA_FLAG = 'Абитуриентам (общие)'
ENROLLEE_FULL_TIME_QA_FLAG = 'Абитуриентам (очная)'
ENROLLEE_PART_TIME_QA_FLAG = 'Абитуриентам (очно-заочная)'
ENROLLEE_EXTRAMURAL_QA_FLAG = 'Абитуриентам (заочная)'

STUDENT_QA_FLAG = 'Студентам (общие)'
STUDENT_FULL_TIME_QA_FLAG = 'Студентам (очная)'
STUDENT_PART_TIME_QA_FLAG = 'Студентам (очно-заочная)'
STUDENT_EXTRAMURAL_QA_FLAG = 'Студентам (заочная)'

QA_FLAGS = [GENERAL_QA_FLAG,
            ENROLLEE_QA_FLAG,
            ENROLLEE_FULL_TIME_QA_FLAG,
            ENROLLEE_PART_TIME_QA_FLAG,
            ENROLLEE_EXTRAMURAL_QA_FLAG,
            STUDENT_QA_FLAG,
            STUDENT_FULL_TIME_QA_FLAG,
            STUDENT_PART_TIME_QA_FLAG,
            STUDENT_EXTRAMURAL_QA_FLAG]


async def get_qa_flags(qa_id: int) -> List[str]:
    question_answer_flag_DAO = QuestionAnswerFlagDAO()
    qa_flag_records = await question_answer_flag_DAO.get_many(qa_id=qa_id)

    qa_flags = []

    for qa_flag_record in qa_flag_records:
        qa_flag_record_dict = dict(qa_flag_record)

        if QA_FLAGS.__contains__(qa_flag_record_dict['QuestionAnswerFlag_flag']):
            qa_flags.append(qa_flag_record_dict['QuestionAnswerFlag_flag'])

    return qa_flags


async def add_flag(qa_id: int, flag: str):
    if QA_FLAGS.__contains__(flag):
        question_answer_flag_DAO = QuestionAnswerFlagDAO()
        await question_answer_flag_DAO.create(qa_id=qa_id, flag=flag)


async def get_or_create_qa_record(question: str, answer: str) -> Record:
    question_answer_DAO = QuestionAnswerDAO()
    qa_record = await question_answer_DAO.get_or_create(question=question, answer=answer)
    return qa_record


async def has_qa_record(id: int) -> bool:
    qa_record = await get_qa_record(id=id)
    return qa_record != None


async def get_qa_record(id: int) -> Record:
    question_answer_DAO = QuestionAnswerDAO()
    qa_record = await question_answer_DAO.get(id=id)
    return qa_record


async def get_all_qa_records() -> List[Record]:
    question_answer_DAO = QuestionAnswerDAO()
    qa_records = await question_answer_DAO.get_many()
    return qa_records


async def get_qa_records_by_flag(flag: str) -> List[Record]:
    qa_records = []
    
    if QA_FLAGS.__contains__(flag):
        question_answer_DAO = QuestionAnswerDAO()
        question_answer_flag_DAO = QuestionAnswerFlagDAO()
        qa_flag_records = await question_answer_flag_DAO.get_many(flag=flag)

        for qa_flag_record in qa_flag_records:
            qa_flag_record_dict = dict(qa_flag_record)
            qa_records.append(await question_answer_DAO.get(id=qa_flag_record_dict["QuestionAnswerFlag_qa_id"]))

        return qa_records


async def remove_qa_record(id: int):
    question_answer_DAO = QuestionAnswerDAO()
    question_answer_flag_DAO = QuestionAnswerFlagDAO()

    if await has_qa_record(id):
        qa_record = await question_answer_DAO.get(id=id)
        qa_record_dict = dict(qa_record)

        qa_flag_records = await question_answer_flag_DAO.get_many(qa_id=int(qa_record_dict["QuestionAnswer_id"]))

        for qa_flag_record in qa_flag_records:
            qa_flag_record_dict = dict(qa_flag_record)
            await question_answer_flag_DAO.delete_by_id(int(qa_flag_record_dict["QuestionAnswerFlag_id"]))

        await question_answer_DAO.delete_by_id(int(qa_record_dict["QuestionAnswer_id"]))


async def get_all_qa_pairs() -> List[QAPair]:
    question_answer_DAO = QuestionAnswerDAO()
    qa_records = await question_answer_DAO.get_many()
    qa_pairs = qa_records_to_pairs(qa_records)
    return qa_pairs


async def get_qa_pairs_by_flag(flag: str):
    qa_pairs = qa_records_to_pairs(await get_qa_records_by_flag(flag))
    return qa_pairs


def qa_records_to_pairs(qa_records: List[Record]) -> List[QAPair]:
    qa_pairs = []
    if qa_records != None:
        for qa_record in qa_records:
            qa_record_dict = dict(qa_record)
            qa_pairs.append(QAPair(qa_record_dict["QuestionAnswer_question"], qa_record_dict["QuestionAnswer_answer"]))

    return qa_pairs
