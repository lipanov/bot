import TextSimilarityRecognition as tsr

class QuestAnswerPair:
    quests = []
    answer = ""

    def __init__(self, quests, answer):
        self.quests = quests
        self.answer = answer


questAnswerPairs = []
questAnswerPairs.append(QuestAnswerPair(["Как дела?", "Как жизнь?"], "Нормально."))
questAnswerPairs.append(QuestAnswerPair(["Ты любишь вареники?"], "Yes."))
questAnswerPairs.append(QuestAnswerPair(["В чём смысл жизни?"], "Я компьютер такое не знаб"))


def getAnswer(quest):
    suitable = None
    suitableCoefficent = 0.6
    for p in questAnswerPairs:
        for q in p.quests:
            coefficent = tsr.getWordsSimilarityCoefficent(q, quest)
            if coefficent > suitableCoefficent:
                suitable = p
                suitableCoefficent = coefficent

    if suitable != None:
        return suitable.answer
    else:
        return None


def find(inp):
    l=inp[6::]
    answer = getAnswer(l)
    if answer is None:
        return "// Ответ на данный вопрос не найден!"
    else:
        return answer


#Объеденил новый код поиска от сани и старый метод поиска в полтора файла: Function и TextSimilarityRecognition

#в мейн
#@dp.message_handler(commands=['find'])
#async def test(msg: types.Message):
#    find(msg.text)
