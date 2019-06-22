from __future__ import print_function
from __future__ import unicode_literals
from builtins import dict
import os
import csv
import re
from corpus.Corpus import Corpus
import sys
# sys.setdefaultencoding('utf-8')

DA_id2desc = {1: "inform",2:"question",3:"directive",4:"commissive"}

#TODO: create Train_val_test set definition csv

class DailyDialog(Corpus):
    def __init__(self, corpus_folder):
        assert os.path.exists(corpus_folder), "the corpus folder for DailyDialog does not exists"

        self.corpus_folder = corpus_folder
        self.csv_corpus = []
        self.tags_list = []

    def load_csv(self):
        subsets = ['train', 'validation', 'test']
        csv_corpus = {}
        tvt_split = {'train':[], 'validation':[], 'test':[]}

        for sset in subsets:
            dial_dir = os.path.join(self.corpus_folder, sset, "dialogues.txt")
            act_dir = os.path.join(self.corpus_folder, sset, "dialogues_act.txt")

            in_dial = open(dial_dir, 'r')
            in_act = open(act_dir, 'r')

            for line_count, (line_dial, line_act) in enumerate(zip(in_dial, in_act)):
                csv_dialogue = []
                # line_dial.decode('utf-8')
                seqs = line_dial.split('__eou__')
                seqs = seqs[:-1]

                acts = line_act.split(' ')
                acts = acts[:-1]
                prev_DAs = {"A":"%", "B":"%"}

                for segment, (utt, act) in enumerate(zip(seqs, acts)):
                    speaker = "A" if segment % 2 == 0 else "B"
                    DA_tag = DA_id2desc[int(act)]

                    csv_dialogue.append((DA_tag, utt, speaker, segment))
                    prev_DAs[speaker] = DA_tag

                csv_corpus["{}_{}".format(sset, line_count)] = csv_dialogue
                tvt_split[sset].append("{}_{}".format(sset, line_count))

        self.csv_corpus = csv_corpus

        # create Train/Val/Test split file
        # split_file_name = os.path.join(self.corpus_folder, "Train_Validation_Test_split.csv")
        # with open(split_file_name, "w") as f:
            # f.write(",test,training,validation\n")
            # for i in range(len(tvt_split['train'])):
                # f.write(str(i)+",")
                # if i < len(tvt_split['test']):
                    # f.write(tvt_split['test'][i])
                # f.write(",")
                # f.write(tvt_split['train'][i])
                # f.write(",")
                # if i < len(tvt_split['validation']):
                    # f.write(tvt_split['validation'][i])
                # f.write("\n")

        self.update_tags()
        return csv_corpus

    def create_csv(self, dialogs):
        subsets = ['train', 'validation', 'test']
        csv_corpus = []

        for sset in subsets:
            dial_dir = os.path.join(self.corpus_folder, sset, 'dialogues.txt')
            act_dir = os.path.join(self.corpus_folder, sset, 'dialogues_act.txt')

            in_dial = open(dial_dir, 'r')
            in_act = open(act_dir, 'r')

            for line_count, (line_dial, line_act) in enumerate(zip(in_dial, in_act)):
                seqs = line_dial.split('__eou__')
                seqs = seqs[:-1]

                acts = line_act.split(' ')
                acts = acts[:-1]
                prev_DAs = {"A":"%", "B":"%"}

                for segment, (utt, act) in enumerate(zip(seqs, acts)):
                    speaker = "A" if segment % 2 == 0 else "B"
                    DA_tag = DA_id2desc[int(act)]

                    csv_corpus.append((utt, DA_tag, prev_DAs[speaker], segment, None, None))
                    prev_DAs[speaker] = DA_tag

        return csv_corpus

    @staticmethod
    def write_csv(to_write, headers, filename="generated_dataset", outpath=""):
        with open(outpath+filename+'.csv','wb') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(headers)
            for line in to_write:
                writer.writerow(line)
        print("Written output csv file: ", filename)


    @staticmethod
    def da_to_dimension(corpus_tuple):
        raise NotImplementedError()

    @staticmethod
    def da_to_cf(corpus_tuple):
        raise NotImplementedError()
