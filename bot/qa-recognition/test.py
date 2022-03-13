from questionFactory import questions

# Выбор алгоритма для теста:
# from answerRecognitionA import recognizeAnswers
# from answerRecognitionB import recognizeAnswers
# from answerRecognitionC import recognizeAnswers
from answerRecognitionD import recognizeAnswers

print("")
print("Вопрос-ответ. Чтобы остановить программу введите команду '/stop'.")

while True:
    print("")
    i = str(input("Введите вопрос или команду:"))

    if i == "/stop":
        break

    answers = recognizeAnswers(i, questions)

    if len(answers) == 0:
        print("// Ответ на данный вопрос не найден!")
    else:
        for a in answers:
            print(a.toString())