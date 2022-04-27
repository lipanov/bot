from asyncpg import Record
from typing import List

from localization import EN_KEY, RU_KEY

from qa_recognition.qa import QAPair

from DAO import QuestionAnswerDAO, QuestionAnswerFlagDAO, QuestionAnswerTagDAO

GENERAL_QA_FLAG = 'Общие'

ENROLLEE_QA_FLAG = 'Абитуриентам'
ENROLLEE_FULL_TIME_QA_FLAG = 'Абитуриентам/Очная'
ENROLLEE_PART_TIME_QA_FLAG = 'Абитуриентам/Очно-заочная'
ENROLLEE_EXTRAMURAL_QA_FLAG = 'Абитуриентам/Заочная'

STUDENT_QA_FLAG = 'Студентам'
STUDENT_FULL_TIME_QA_FLAG = 'Студентам/Очная'
STUDENT_PART_TIME_QA_FLAG = 'Студентам/Очно-заочная'
STUDENT_EXTRAMURAL_QA_FLAG = 'Студентам/Заочная'

RAW_QA_FLAGS = [GENERAL_QA_FLAG,
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

        flag = qa_flag_record_dict['QuestionAnswerFlag_flag']
        raw_flag = flag_to_raw(flag)

        if raw_flag in RAW_QA_FLAGS:
            qa_flags.append(qa_flag_record_dict['QuestionAnswerFlag_flag'])

    return qa_flags


async def add_flag(qa_id: int, flag: str):
    raw_flag = flag_to_raw(flag)

    if raw_flag in RAW_QA_FLAGS:
        question_answer_flag_DAO = QuestionAnswerFlagDAO()
        await question_answer_flag_DAO.create(qa_id=qa_id, flag=flag)


async def get_qa_records_by_flag(flag: str) -> List[Record]:
    qa_records = []
    raw_flag = flag_to_raw(flag)
    
    if raw_flag in RAW_QA_FLAGS:
        question_answer_DAO = QuestionAnswerDAO()
        question_answer_flag_DAO = QuestionAnswerFlagDAO()
        qa_flag_records = await question_answer_flag_DAO.get_many(flag=flag)

        for qa_flag_record in qa_flag_records:
            qa_flag_record_dict = dict(qa_flag_record)
            qa_records.append(await question_answer_DAO.get(id=qa_flag_record_dict["QuestionAnswerFlag_qa_id"]))

    return qa_records


def flag_to_raw(flag: str) -> str:
    if RU_KEY + "/" in flag:
        flag = flag.replace(RU_KEY + "/", "")
    if EN_KEY + "/" in flag:
        flag = flag.replace(EN_KEY + "/", "")

    return flag


async def get_tags(qa_id: int) -> List[str]:
    question_answer_tag_DAO = QuestionAnswerTagDAO()
    tags = []
    qa_tag_records = await question_answer_tag_DAO.get_many(qa_id=qa_id)

    for record in qa_tag_records:
        record_dict = dict(record)
        tags.append(record_dict["QuestionAnswerTag_tag"])

    return tags


async def set_tags(qa_id: int, tags: List[str]):
    question_answer_tag_DAO = QuestionAnswerTagDAO()

    await clear_tags(qa_id)
    
    for tag in tags:
        await question_answer_tag_DAO.create(qa_id=qa_id, tag=tag)


async def clear_tags(qa_id: int):
    question_answer_tag_DAO = QuestionAnswerTagDAO()

    qa_tag_records = await question_answer_tag_DAO.get_many(qa_id=qa_id)
    ids = [dict(record)["QuestionAnswerTag_id"] for record in qa_tag_records]

    for id in ids:
        await question_answer_tag_DAO.delete_by_id(id)


async def has_qa(id: int) -> bool:
    qa_record = await get_qa_record(id=id)
    return qa_record != None


async def get_qa_record(id: int) -> Record:
    question_answer_DAO = QuestionAnswerDAO()
    qa_record = await question_answer_DAO.get(id=id)
    return qa_record


async def create_qa(question: str, answer: str) -> Record:
    question_answer_DAO = QuestionAnswerDAO()
    qa_record = await question_answer_DAO.get_or_create(question=question, answer=answer)
    return qa_record


async def get_all_qa_records() -> List[Record]:
    question_answer_DAO = QuestionAnswerDAO()
    qa_records = await question_answer_DAO.get_many()
    return qa_records


async def remove_qa(id: int):
    question_answer_DAO = QuestionAnswerDAO()
    question_answer_flag_DAO = QuestionAnswerFlagDAO()

    if await has_qa(id):
        qa_record = await question_answer_DAO.get(id=id)
        qa_record_dict = dict(qa_record)

        qa_flag_records = await question_answer_flag_DAO.get_many(qa_id=int(qa_record_dict["QuestionAnswer_id"]))

        for qa_flag_record in qa_flag_records:
            qa_flag_record_dict = dict(qa_flag_record)
            await question_answer_flag_DAO.delete_by_id(int(qa_flag_record_dict["QuestionAnswerFlag_id"]))

        await clear_tags(id)
        await question_answer_DAO.delete_by_id(int(qa_record_dict["QuestionAnswer_id"]))


async def get_qa_pair(qa_id: int) -> QAPair:
    if await has_qa(qa_id):
        return await qa_record_to_pair(await get_qa_record(qa_id))
    else:
        return None


async def get_all_qa_pairs() -> List[QAPair]:
    qa_records = await get_all_qa_records()
    qa_pairs = await qa_records_to_pairs(qa_records)

    qa_pairs.sort(key=lambda x: x.id)

    return qa_pairs


async def get_qa_pairs_by_flag(flag: str):
    qa_pairs = await qa_records_to_pairs(await get_qa_records_by_flag(flag))
    return qa_pairs


async def qa_records_to_pairs(records: List[Record]) -> List[QAPair]:
    qa_pairs = []

    for record in records:
        qa_pairs.append(await qa_record_to_pair(record))

    return qa_pairs


async def qa_record_to_pair(record: Record) -> QAPair:
    record_dict = dict(record)

    id = record_dict["QuestionAnswer_id"]
    question = record_dict["QuestionAnswer_question"]
    answer = record_dict["QuestionAnswer_answer"]
    tags = await get_tags(id)

    return QAPair(id, question, answer, tags)
