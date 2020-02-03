import os
import json


def read_all_lines(path):
    with open(path, 'r') as read_file:
        all_lines_list = json.load(read_file)
    return all_lines_list


def split_train_test(trigrams_file, train_percentage, output_path):
    all_lines=open(trigrams_file,'r').readlines()
    data_size = len(all_lines)
    print(data_size)
    train_size = round(data_size * train_percentage)
    test_size = data_size - train_size
    open_train_file = open(output_path+'train.csv','w')
    open_test_file = open(output_path+'test.csv','w')
    for idx in range(train_size):
        print(idx)
        open_train_file.write(all_lines[idx])
    for idx in range(train_size, data_size):
        print(idx)
        open_test_file.write(all_lines[idx])


def get_labelled_trigrams(path, trigrams_output_file):
    all_lines_list = read_all_lines(path)
    trigrams_file = open(trigrams_output_file, 'w')
    datasize = len(all_lines_list)
    for lidx, line in enumerate(all_lines_list):
        sentence = str.strip(line[0])
        sentence=sentence.replace('...','')
        sentence = sentence.replace('..', '.')
        sentence = sentence.replace('. .', '.')
        dot_splitted_sentence = sentence.split('.')
        num_segments = len(dot_splitted_sentence)
        if num_segments > 2:
            for idx, seg in enumerate(dot_splitted_sentence):
                if idx < num_segments - 2:
                    part1 = str.strip(seg).split(' ')[-1]
                    part2 = str.strip(dot_splitted_sentence[idx + 1]).split(' ')[0]
                    trigram = part1 + '\t.\t' + part2
                    trigrams_file.write(trigram + '\t' + '0' + '\n')
                elif idx == num_segments - 2:
                    if lidx < datasize - 1:
                        part1 = str.strip(seg).split(' ')[-1]
                        part2 = str.strip(all_lines_list[lidx + 1][0]).split(' ')[0].split('.')[0]
                        trigram = part1 + '\t.\t' + part2
                        trigrams_file.write(trigram + '\t' + '1' + '\n')

        else:
            if lidx < datasize - 1:
                part1= str.strip(dot_splitted_sentence[0]).split(' ')[-1]
                part2= str.strip(all_lines_list[lidx + 1][0]).split(' ')[0].split('.')[0]
                trigram = part1 + '\t.\t' + part2
                trigrams_file.write(trigram + '\t' + '1' + '\n')


if __name__ == '__main__':
    raw_data_path = os.environ['HOME'] + '/SupervisedSB/penn-treebank-master/penn-data.json'
    labelled_trigrams_file = os.environ['HOME'] + '/SupervisedSB/data/labelled_trigrams.csv'
    get_labelled_trigrams(raw_data_path, labelled_trigrams_file)
    #split_train_test(os.environ['HOME'] + '/SupervisedSB/data/labelled_trigrams.csv', 0.8, os.environ['HOME'] + '/SupervisedSB/data/')
