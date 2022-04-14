from typing import Dict, List

from qa_recognition.qa import QAPair, Answer


class Router:
    async def get_most_relevant_answer(question: str, qa_pairs: List[QAPair]) -> Answer:
        pass

    async def get_most_relevant_answers(question: str, qa_pairs: List[QAPair]) -> List[Answer]:
        pass
