from asyncpg import Record
from typing import List

from qa_recognition.qa import QAPair

from DAO import QuestionAnswerDAO, QuestionAnswerGroupDAO


async def get_qa_groups(qa_id: int) -> List[str]:
    question_answer_group_DAO = QuestionAnswerGroupDAO()
    qa_group_records = await question_answer_group_DAO.get_many(qa_id=qa_id)

    qa_gorups = []

    for qa_group_record in qa_group_records:
        qa_group_record_dict = dict(qa_group_record)
        qa_gorups.append(qa_group_record_dict["QuestionAnswerGroup_group_title"])

    return qa_gorups


async def add_qa_to_group(qa_id: int, group_title: str):
    question_answer_group_DAO = QuestionAnswerGroupDAO()
    await question_answer_group_DAO.create(qa_id=qa_id, group_title=group_title)


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


async def get_qa_records_by_group(group_title: str) -> List[Record]:
    question_answer_DAO = QuestionAnswerDAO()
    question_answer_group_DAO = QuestionAnswerGroupDAO()

    qa_records = []
    qa_group_records = await question_answer_group_DAO.get_many(group_title=group_title)

    for qa_group_record in qa_group_records:
        qa_group_record_dict = dict(qa_group_record)
        qa_records.append(await question_answer_DAO.get(id=qa_group_record_dict["QuestionAnswerGroup_qa_id"]))

    return qa_records


async def remove_qa_record(id: int):
    question_answer_DAO = QuestionAnswerDAO()
    question_answer_group_DAO = QuestionAnswerGroupDAO()

    if await has_qa_record(id):
        qa_record = await question_answer_DAO.get(id=id)
        qa_record_dict = dict(qa_record)

        qa_group_records = await question_answer_group_DAO.get_many(qa_id=int(qa_record_dict["QuestionAnswer_id"]))

        for qa_group_record in qa_group_records:
            qa_group_record_dict = dict(qa_group_record)
            await question_answer_group_DAO.delete_by_id(int(qa_group_record_dict["QuestionAnswerGroup_id"]))

        await question_answer_DAO.delete_by_id(int(qa_record_dict["QuestionAnswer_id"]))


async def get_all_qa_pairs() -> List[QAPair]:
    question_answer_DAO = QuestionAnswerDAO()
    qa_records = await question_answer_DAO.get_many()
    qa_pairs = qa_records_to_pairs(qa_records)
    return qa_pairs


async def get_qa_pairs_by_group(group_title: str):
    qa_pairs = qa_records_to_pairs(await get_qa_records_by_group(group_title))
    return qa_pairs


def qa_records_to_pairs(qa_records: List[Record]) -> List[QAPair]:
    qa_pairs = []
    if qa_records != None:
        for qa_record in qa_records:
            qa_record_dict = dict(qa_record)
            qa_pairs.append(QAPair(qa_record_dict["QuestionAnswer_question"], qa_record_dict["QuestionAnswer_answer"]))

    return qa_pairs
