from typing import List
from qa_recognition.qa import Answer, QAPair, getTagsByText
from qa_recognition.jakkards_coefficent import calculateJakkardsCoefficent, calculateStringsJakkardsCoefficent

class AnswerRecognizer:
    weight : int = 0

    def get_key(self) -> str:
        pass


    def recognize_answers(self, question : str, qaPairs : List[QAPair]) -> List[Answer]:
        pass


class AAlgorithmAnswerRecognizer(AnswerRecognizer):
    def get_key(self) -> str:
        return "A_Algorithm"


    def MIN_ANSWER_CHANCE(self) -> float:
        return 0.6


    def recognize_answers(self, question : str, qaPairs : List[QAPair]) -> List[Answer]:
        answers = []
        lastAnswerChance = self.MIN_ANSWER_CHANCE()

        for qaPair in qaPairs:
            coefficent = calculateStringsJakkardsCoefficent(question, qaPair.question)
            if coefficent > lastAnswerChance:
                answers.append(Answer(qaPair.answer, self.get_key(), coefficent))
                lastAnswerChance = coefficent

        answers.reverse()
        return answers


class BAlgorithmAnswerRecognizer(AnswerRecognizer):
    def get_key(self) -> str:
        return "B_Algorithm"


    def MIN_SIMILAR_TAGS_COUNT(self) -> int:
        return 2


    def MIN_TAG_SIMILARITY(self) -> float:
        return 0.5


    def recognize_answers(self, question : str, qaPairs : List[QAPair]) -> List[Answer]:
        targetTags = getTagsByText(question)
        answers = []
        lastSimilarTagsCount = self.MIN_SIMILAR_TAGS_COUNT()

        for qaPair in qaPairs:
            questionTags = qaPair.getTags()
            similarTagsCount = 0

            for targetTag in targetTags:
                for questionTag in questionTags:
                    if calculateStringsJakkardsCoefficent(targetTag, questionTag) > self.MIN_TAG_SIMILARITY():
                        similarTagsCount += 1
            
            if similarTagsCount >= lastSimilarTagsCount:
                coefficent = calculateJakkardsCoefficent(len(targetTags), len(questionTags), similarTagsCount)
                answers.append(Answer(qaPair.answer, self.get_key(), coefficent))
                lastSimilarTagsCount = similarTagsCount

        answers.reverse()
        return answers


class CAlgorithmAnswerRecognizer(AnswerRecognizer):
    def get_key(self) -> str:
        return "C_Algorithm"


    def MIN_TAG_SIMILARITY(self):
        return 0.5


    def MIN_ANSWER_SIMILARITY(self) -> float:
        return 0.5


    def recognize_answers(self, question : str, qaPairs : List[QAPair]) -> List[Answer]:
        targetTags = getTagsByText(question)
        answers = []
        lastSimilarity = self.MIN_ANSWER_SIMILARITY()

        for qaPair in qaPairs:
            questionTags = qaPair.getTags()
            similarTagsCount = 0

            for targetTag in targetTags:
                for questionTag in questionTags:
                    if calculateStringsJakkardsCoefficent(targetTag, questionTag) > self.MIN_TAG_SIMILARITY():
                        similarTagsCount += 1

            coefficent = calculateJakkardsCoefficent(len(targetTags), len(questionTags), similarTagsCount)
            
            if coefficent > lastSimilarity:
                answers.append(Answer(qaPair.answer, self.get_key(), coefficent))
                lastSimilarity = coefficent

        answers.reverse()
        return answers

    
class DAlgorithmAnswerRecognizer(AnswerRecognizer):
    def get_key(self) -> str:
        return "D_Algorithm"
            

    def MIN_SIMILAR_TAGS_COUNT(self) -> int:
        return 2


    def MIN_TAG_SIMILARITY(self) -> float:
        return 0.5
        

    def MIN_ANSWER_SIMILARITY(self) -> float:
        return 0.7


    def recognize_answers(self, question : str, qaPairs : List[QAPair]) -> List[Answer]:
        targetTags = getTagsByText(question)
        answers = []
        lastSimilarity = self.MIN_ANSWER_SIMILARITY()
        lastSimilarTagsCount = self.MIN_SIMILAR_TAGS_COUNT()

        for qaPair in qaPairs:
            questionTags = qaPair.getTags()
            similarTagsCount = 0

            for targetTag in targetTags:
                for questionTag in questionTags:
                    if calculateStringsJakkardsCoefficent(targetTag, questionTag) > self.MIN_TAG_SIMILARITY():
                        similarTagsCount += 1

            coefficent = calculateJakkardsCoefficent(len(targetTags), len(questionTags), similarTagsCount)

            if similarTagsCount > lastSimilarTagsCount and coefficent > lastSimilarity:
                answers.append(Answer(qaPair.answer, self.get_key(), coefficent))
                lastSimilarity = coefficent
                lastSimilarTagsCount = similarTagsCount

        answers.reverse()
        return answers