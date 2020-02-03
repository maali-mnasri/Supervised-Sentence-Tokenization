import pickle
from TrainSBModel import trigram_featurizer
import argparse


def sentence_tokenizer(text, classifierpath):
    classifier = load_classifier(classifierpath)
    sentences = []
    sentence=''
    text.replace('...', '')
    text.replace('..', '')
    text.replace('. .', '')
    #print(text)
    dot_splitted_text = text.split('.')
    for idx, seg in enumerate(dot_splitted_text):
        if idx < len(dot_splitted_text) - 2:
            part1 = str.strip(seg).split(' ')[-1]
            part2 = str.strip(dot_splitted_text[idx + 1]).split(' ')[0]
            boundary_trigram = part1 + '\t.\t' + part2
            #print(boundary_trigram)
            features_vector = trigram_featurizer(boundary_trigram.split())
            #print(features_vector)
            prediction = classifier.predict([features_vector])
            #print(prediction)
            if prediction == [1] :
                #print('yes')
                sentence += seg+'.'
                sentences.append(sentence)
                sentence = ''
            else:
                sentence += seg+'.'
        else:
            sentence += seg
            sentences.append(sentence)
            sentence = ''
    for s in sentences:
        print(s)
    return sentences


def load_classifier(path):
    modelfile = open(path, 'rb')
    return pickle.load(modelfile, encoding='latin1')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", help="the text to segment into sentences")
    args = parser.parse_args()
    #text='At least 28 people are confirmed to have corona till today, says Mr. Guhang at the health summit. Three new cases have been diagnosed in U. K. this morning.' \
    #    'The syptoms remain unclear but a fever beyond 37.5 degrees is a bad sign. '
    if args.text:
        sents = sentence_tokenizer(args.text,'../data/SB_Classifier')