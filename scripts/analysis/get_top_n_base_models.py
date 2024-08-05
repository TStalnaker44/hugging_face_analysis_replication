from ..utilities.querier import Querier

def main():

    q = Querier()
    baseFreqs = q.getBaseModelFrequencies()

    #Set n for the top-n
    n = 10

    #Print the top-n most frequently declared base models and their information
    for i in baseFreqs.most_common(n):
        model = q.getModelById(i[0])
        print(model['name'] + " declared as a base model " + str(i[1]) + " times; licensed under " + str(model['licenses']) + ", " + str(model['likes']) + " likes, " + str(model['downloads']) + " downloads")

