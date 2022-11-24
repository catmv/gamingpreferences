import numpy as np
import math as m
import copy as cp
import csv
import random
import sys

print("\n\n")

sn = int(sys.argv[1])
print("processing subject number:", sn)
print("\n\n")

weightMap = [4,3,3,2,3,5,4,1,3,3,4,4,3,2,3,2,3,2,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,3]

gamesOrder = np.loadtxt('gamesOrder.txt', dtype='str', delimiter=';')
gameQuestionsOrder = np.loadtxt('gameQuestions.txt', dtype='str', delimiter=';')
gameFeatures = np.loadtxt('gameFeatures.csv', dtype='str', delimiter=';')
featuresMap = np.loadtxt('featuresMap.csv', dtype='str', delimiter=';')

featuresMapDict = {}
for f in featuresMap:
    featuresMapDict[f[0]] = int(f[1])

gameFeaturesNum = np.zeros((gamesOrder.shape[0], gameQuestionsOrder.shape[0])).astype('int')

for i, game in enumerate(gameFeatures):
    for j, feature in enumerate(game):
        gameFeaturesNum[i, j] = featuresMapDict[feature]

#print(gameFeaturesNum)

similarityMatrix = np.zeros((gamesOrder.shape[0], gamesOrder.shape[0]))
for i in range(gameFeaturesNum.shape[0]):
    for j in range(i, gameFeaturesNum.shape[0]):
        score = 0
        for k in range(gameFeaturesNum.shape[1]):
            if gameFeaturesNum[i, k] == gameFeaturesNum[j, k]:
                score = score + 1
        similarityMatrix[i, j] = score
        similarityMatrix[j, i] = score

#print("similarityMatrix\n")
#print(similarityMatrix)
#print("\n")

# query = np.loadtxt("query.csv", dtype='int', delimiter=' ')
#
# query = gameFeaturesNum[7, :]
#
# def getRecomendation(q):
#     scoreMatrix = np.zeros((gamesOrder.shape[0], 2)).astype('int')
#     for i, game in enumerate(gameFeaturesNum):
#         score = 0
#         for j, feature in enumerate(game):
#             if q[j] == feature:
#                 score = score + 1
#         scoreMatrix[i, 0] = i
#         scoreMatrix[i, 1] = score
#
#     order = np.argsort(scoreMatrix, axis=0)
#     orderReverse = order[::-1, 1]
#
#     output = np.stack((gamesOrder[orderReverse, 1], scoreMatrix[orderReverse, 1]), axis=1)
#
#     return output
#
# print(getRecomendation(query))

# rFile = open("Preferências de Videojogos e relação com características de personalidade.csv", 'r')
# rFile.readline()
# rLines = rFile.readlines()
# lastLine = rLines[-1]
# responses = csv.reader([lastLine], delimiter=',', quotechar='"')


def getSubjectResponses(s):

    rFile = open("Preferências de Videojogos e relação com características de personalidade.csv", 'r')
    rFile.readline()
    rLines = rFile.readlines()

    responseList = []

    for ln, line in enumerate(rLines):
        l = line
        responses = csv.reader([l], delimiter=',', quotechar='"')
        for row in responses:
            for i, item in enumerate(row):
                if i == 2 and int(item) == s:
                    good = csv.reader([l], delimiter=',', quotechar='"')
                    for row in good:
                        for k, el in enumerate(row):
                            responseList.append(el)
                    return responseList


    print("SUBJECT NOT FOUND !!!!")
    quit()



rl = getSubjectResponses(sn)

#print("starting map\n\n")

def getResponseMap(r):
    map = []

    #Q0 Players of this game are generally...
    hardcoreScore = 0
    betweenScore = 0
    casualScore = 0
    if r[7] == "Todos os dias":
        hardcoreScore = hardcoreScore + 1
    elif r[7] == "Todas as semanas":
        betweenScore = betweenScore + 1
    else:
        casualScore = casualScore + 1

    if r[8] == "Gamer hardcore":
        hardcoreScore = hardcoreScore + 1
    elif r[8] == "Algo entre hardcore e casual":
        betweenScore = betweenScore + 1
    else:
        casualScore = casualScore + 1

    if r[11] == "Mais de 10 horas por semana":
        hardcoreScore = hardcoreScore + 1
    elif r[11] == "5-10 horas por semana":
        betweenScore = betweenScore + 1
    else:
        casualScore = casualScore + 1

    if hardcoreScore > betweenScore and hardcoreScore > casualScore:
        print("ok0")
        map.append(1)
    if betweenScore >= hardcoreScore and betweenScore > casualScore:
        print("ok0")
        map.append(2)
    if casualScore >= hardcoreScore and casualScore >= betweenScore:
        print("ok0")
        map.append(3)

    #Q1 The perspective of this game is...
    if r[14] == "1st person":
        print("ok1")
        map.append(1)
    else:
        print("ok1")
        map.append(2)

    #Q2 This game is...single/Multiplayer
    if r[9] == "Jogos single player, em que jogo sozinho/a":
        print("ok2")
        map.append(1)
    elif r[9] == "Jogos single player, mas às vezes peço ajuda a outras pessoas":
        print("ok2")
        map.append(1)
    elif r[9] == "Não sei":
        print("ok2")
        map.append(1)
    else:
        print("ok2")
        map.append(2)

    #Q3 For which platform is this game available?
    if r[10] == "PC":
        print("ok3")
        map.append(1)
    elif r[10] == "Telemóvel e/ou tablet":
        print("ok3")
        map.append(2)
    elif r[10] == "PlayStation":
        print("ok3")
        map.append(3)
    elif r[10] == "Nintendo Switch":
        print("ok3")
        map.append(4)
    elif r[10] == "Xbox":
        print("ok3")
        map.append(5)
    elif r[10] == "Nintendo Wii":
        print("ok3")
        map.append(6)
    elif r[10] == "Não costumo jogar":
        print("ok3")
        map.append(7)
    else:
        print("ok3")
        map.append(7)

    #Q4 This game is usually played...long/short
    short = 0
    medium = 0
    long = 0
    if r[13] == "Curto/Repetitivo":
        short = short + 1
    elif r[13] == "Médio":
        medium = medium + 1
    elif r[13] == "Longo":
        long = long + 1
    else:
        short = short + 1

    if r[12] == "Nunca jogo videojogos":
        short = short + 1
    elif r[12] == "Menos de 30 minutos":
        short = short + 1
    elif r[12] == "Entre 30 minutos a 1 hora":
        medium = medium + 1
    elif r[12] == "1 a 2 horas":
        medium = medium + 1
    else:
        long = long + 1

    if long > medium and long > short:
        print("ok4")
        map.append(1)
    if medium >= long and medium > short:
        print("ok4")
        map.append(2)
    if short >= long and short >= medium:
        print("ok4")
        map.append(3)

    #Q5 This game can be classified as belonging to the following genre:
    if r[15] == "Ação":
        print("ok5")
        map.append(1)
    elif r[15] == "Aventura":
        print("ok5")
        map.append(2)
    elif r[15] == "Desporto":
        print("ok5")
        map.append(12)
    elif r[15] == "Música/Ritmo":
        print("ok5")
        map.append(9)
    elif r[15] == "Simulação":
        print("ok5")
        map.append(11)
    elif r[15] == "First-person Shooter":
        print("ok5")
        map.append(15)
    elif r[15] == "MMORPG":
        print("ok5")
        map.append(5)
    elif r[15] == "RPG":
        print("ok5")
        map.append(10)
    elif r[15] == "Puzzle/Casual/Cartas":
        print("ok5")
        map.append(3)
    elif r[15] == "Visual Novels/Dating Sims":
        print("ok5")
        map.append(14)
    elif r[15] == "Racing":
        print("ok5")
        map.append(8)
    elif r[15] == "Platformer":
        print("ok5")
        map.append(7)
    elif r[15] == "Fighting":
        print("ok5")
        map.append(4)
    elif r[15] == "Estratégia":
        print("ok5")
        map.append(13)
    elif r[15] == "Nenhum dos anteriores/Não sei":
        print("ok5")
        map.append(16)
    else:
        print("ok5")
        map.append(16)

    #Q6 This game's graphic style is...
    if r[16] == "Stardew Valley - Pixelated, retro 8-bit, top down":
        print("ok6")
        map.append(4)
    elif r[16] == "The Sims 4 - 3D, cartoony":
        print("ok6")
        map.append(3)
    elif r[16] =="Wii Sports Resort - 3D, low-poly":
        print("ok6")
        map.append(5)
    elif r[16] == "The Witcher - 3D, foto-realista":
        print("ok6")
        map.append(6)
    elif r[16] == "New Super Mario Bros. U Deluxe - 2D flat sideview com modelos 3D lowpoly":
        print("ok6")
        map.append(9)
    elif r[16] == "Atelier Ryza - 3D, Cel-shaded, Anime":
        print("ok6")
        map.append(8)
    elif r[16] == "Danganronpa - 2.5D Anime":
        print("ok6")
        map.append(2)
    elif r[16] == "Call of Duty - 3D, foto-realista":
        print("ok6")
        map.append(6)
    else:
        print("ok6")
        map.append(10)

    #Q7 Does this game require a paid subscription?
    #ignore
    print("ok7")
    map.append(-1)

    #Q8 - end
    for i in range(17, 43):
        map.append(int(r[i]))

    print("map len = ", len(map))
    return map

myMap = getResponseMap(rl)

#print("calculate ranking")
def getRankings(rm):
    scores = np.zeros((gamesOrder.shape[0], 2)).astype('int')
    for i, game in enumerate(gameFeaturesNum):
        gameScore = 0
        for j, feature in enumerate(game):
            if rm[j] == feature:
                gameScore = gameScore + 1*weightMap[j]
        scores[i, 0] = i
        scores[i, 1] = gameScore

    order = np.argsort(scores, axis=0)
    orderReverse = order[::-1, 1]

    output = np.stack((gamesOrder[orderReverse, 1], scores[orderReverse, 1]), axis=1)

    return output

print("similarity ranking:")
recomendation = getRankings(myMap)
print(recomendation)
print("\n\n")
print("recomended games:")
print(recomendation[0])
print(recomendation[random.randint(1, len(recomendation)-1)])
