import os
import csv
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F

from typing import List

from qa_recognition.qa import Answer, QAPair
from qa_recognition.answer_recognizers import AnswerRecognizer
from qa_recognition.network.bert_classifier import BertClassifier

from sklearn.model_selection import train_test_split


class NetworkAnswerRecognizer(AnswerRecognizer):
    KEY = "Network"
    OUTPUT_FOLDER = os.path.join('temp', 'network')
    MODEL_PATH = os.path.join(OUTPUT_FOLDER, 'bert.pt')
    RAW_DATA_PATH = os.path.join(OUTPUT_FOLDER, 'raw_data.csv')
    QA_IDS_PATH = os.path.join(OUTPUT_FOLDER, 'qa_ids.csv')

    def __init__(self) -> None:
        self.init_classifier()

    def init_classifier(self):
        if self.has_required_data() or True:
            qa_ids = pd.read_csv(self.QA_IDS_PATH)

            self.classifier = BertClassifier(
                    model_path='cointegrated/rubert-tiny',
                    tokenizer_path='cointegrated/rubert-tiny',
                    n_classes=len(qa_ids["Label"]) + 1,
                    epochs=2,
                    model_save_path=self.MODEL_PATH
                    )

            if self.has_model() or True:
                #self.classifier = torch.load(self.MODEL_PATH, map_location=torch.device('cpu'))
                self.classifier.load_saved_model()

    def has_required_data(self) -> bool:
        return os.path.exists(self.RAW_DATA_PATH) and os.path.exists(self.QA_IDS_PATH)

    def has_model(self) -> bool:
        return os.path.exists(self.MODEL_PATH)

    def clear_model(self):
        os.remove(self.MODEL_PATH)
    
    def clear_data(self):
        os.remove(self.RAW_DATA_PATH)
        os.remove(self.QA_IDS_PATH)

    def write_data(self, qa_pairs: List[QAPair]):
        if not os.path.exists(self.OUTPUT_FOLDER):
            os.makedirs(self.OUTPUT_FOLDER, exist_ok=True)

        with open(self.RAW_DATA_PATH, "w") as file:
            writer = csv.writer(file)
            writer.writerow(("Question", "Label"))

            i = 1
            for qa in qa_pairs:
                writer.writerow((qa.question, i))

                for tag in qa.tags:
                    writer.writerow((tag, i))

                i += 1

        with open(self.QA_IDS_PATH, "w") as file:
            writer = csv.writer(file)
            writer.writerow(("Label", "Id"))

            i = 1
            for qa in qa_pairs:
                writer.writerow((i, qa.id))
                i += 1

        if self.has_model():
            self.clear_model()
        
        self.init_classifier()

    def train(self):
        if self.has_required_data():
            raw_data = pd.read_csv(self.RAW_DATA_PATH)

            X_train, X_test, y_train, y_test = train_test_split( raw_data['Question'], raw_data['Label'], test_size=0.5, random_state=42)

            self.classifier.preparation(
                    X_train=list(X_train),
                    y_train=list(y_train),
                    X_valid=list(X_test),
                    y_valid=list(y_test)
                    )

            self.classifier.train()

    def recognize_answers(self, question: str, qa_pairs: List[QAPair]) -> List[Answer]:
        answers = []

        if self.has_required_data():
            if self.has_model():
                qa_ids = pd.read_csv(self.QA_IDS_PATH)

                output = self.classifier.predict_raw_output(question.lower())
                argmax = torch.argmax(output.logits, dim=1).cpu().numpy()[0]

                predictions = output.logits.cpu().detach()[0]
                predictions = predictions - torch.min(predictions)
                predictions = F.normalize(predictions, p=1, dim=0)

                result_id = -1

                for label, id in qa_ids.values.tolist():
                    if label == argmax:
                        result_id = id

                for qa in qa_pairs:
                    if qa.id == result_id:
                        answers.append(Answer(qa, self.KEY, predictions[argmax].item()))
                        break

        return answers
