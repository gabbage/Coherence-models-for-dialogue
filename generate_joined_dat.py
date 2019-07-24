from collections import defaultdict
import os, errno
import argparse

def create_path(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    return filename

def read_test_file(path):
    query_id = None
    with open(path, 'r') as infile:
        for line in infile:
            if line[0] is not '#':
                yield query_id, line.strip().split()
            else:
                query_id = line.strip().split()[2]

def read_test_file_2_dict(path):
    query_dict = dict()
    with open(path, 'r') as infile:
        current_query_id = None
        for line in infile:
            if line[0] is not '#':
                query_dict[current_query_id].append(line.strip().split())
            else:
                current_query_id = line.strip().split()[2]
                query_dict[current_query_id] = []
    return query_dict

def combine_files_dict(egrid_dict, noents_dict, trans):
    trans2feat = {'2': 16}
    max_trans_feat = trans2feat.get(trans)
    docs_to_write = defaultdict(list)
    missing = 0

    for doc_id in egrid_dict.keys():
        if doc_id not in noents_dict:
            missing += 1
            continue

        egrid_i_feat_list = egrid_dict[doc_id]
        noent_i_feat_list = noents_dict[doc_id]
        if len(egrid_i_feat_list) != len(noent_i_feat_list):
            missing += 1
            continue

        for i in range(len(egrid_i_feat_list)):
            egrid_i_feat = egrid_i_feat_list[i]
            noent_i_feat = noent_i_feat_list[i]
            label = egrid_i_feat[0]
            qid = egrid_i_feat[1]

            egrid_features = [(f_i.split(':')[0], f_i.split(':')[1]) for f_i in egrid_i_feat[2:]]
            mod_noents_features = [(int(f_i.split(':')[0])+max_trans_feat, f_i.split(':')[1]) for f_i in noent_i_feat[2:]]

            joined_i = (label, qid, egrid_features+mod_noents_features)
            docs_to_write[doc_id].append(joined_i)
        # print('Joined: ', joined_i)

    print("Missing Combinations: {}".format(missing))
    return docs_to_write

def combine_files(egrid_file, noents_file, trans):
    trans2feat = {'2': 16}
    max_trans_feat = trans2feat.get(trans)
    docs_to_write = defaultdict(list)

    for i, egrid_info in enumerate(egrid_file):

        noents_info = noents_file[i]
        # print(egrid_info)
        # print(noents_info)
        doc_id, egrid_i_feat = egrid_info
        doc_id_noent, noent_i_feat = noents_info

        label = egrid_i_feat[0]
        qid = egrid_i_feat[1]

        if doc_id!=doc_id_noent or label!=noent_i_feat[0] or qid!=noent_i_feat[1]:
            print('Doc id: ', doc_id, ' Doc noent: ', doc_id_noent)
            print('Label : ', label, ' Label no ent: ', noent_i_feat[0])
            print('Qid : ', qid, ' Qid no ent: ', noent_i_feat[1])
            raise TypeError('Matching failed between the two files')


        egrid_features = [(f_i.split(':')[0], f_i.split(':')[1]) for f_i in egrid_i_feat[2:]]
        mod_noents_features = [(int(f_i.split(':')[0])+max_trans_feat, f_i.split(':')[1]) for f_i in noent_i_feat[2:]]

        joined_i = (label, qid, egrid_features+mod_noents_features)
        docs_to_write[doc_id].append(joined_i)
        # print('Joined: ', joined_i)

    return docs_to_write

def write_to_dat(docs_to_write, outpath):
    with open(outpath, 'w') as to_write:
        for doc_id, infos in docs_to_write.items():
            to_write.write('# query ' + str(doc_id) + '\n')
            for info_i in infos:
                label = info_i[0]
                query_i = info_i[1]
                features = info_i[2]

                to_write.write(str(label) + " " + str(query_i))
                for feat_ind, feat_val in features:
                    to_write.write(" " + str(feat_ind) + ":" + str(feat_val))
                to_write.write('\n')

def parse():
    parser = argparse.ArgumentParser(description='Feature vectors combinator')
    parser.add_argument('-g', '--generate_feature_vectors', default='Oasis', help='Generate feature vectors')
    parser.add_argument('-m1', '--grid_mode1', default='egrid_-coref', help='Grid mode')
    parser.add_argument('-m2', '--grid_mode2', default='egrid_-coref_DAspan_da_noentcol', help='Grid mode')
    parser.add_argument('-ta', '--task', default='reordering',
                        help='Task type')  # possible values: reordering, insertion
    args = parser.parse_args()
    return args

def main():
    args = parse()

    corpus = args.generate_feature_vectors
    exper_path = 'experiments/'
    egrid = args.grid_mode1
    # egrid = 'simple_egrid_-coref'
    # egrid = 'egrid_-coref'
    noents = args.grid_mode2
    task = args.task
    saliency = 1
    trans = '2'
    data_types = ['test', 'train', 'dev']
    # data_types = ['test']
    # joined_name = 'egrid+noents'
    joined_name = "{}+noents".format(args.grid_mode1)

    for data_type in data_types:

        path_noents = exper_path + corpus + '/' + task + '/' + noents + '/' + corpus + '_sal' + str(
            saliency) + '_range' + trans + "_" + trans + "_" + data_type + '.dat'
        path_egrid = exper_path + corpus + '/' + task + '/' + egrid + '/' + corpus + '_sal' + str(
            saliency) + '_range' + trans + "_" + trans + "_" + data_type + '.dat'
        joined_path = create_path(exper_path + corpus + '/' + task + '/' + joined_name + '/' + corpus + '_sal' + str(
            saliency) + '_range' + trans + "_" + trans + "_" + data_type + '.dat')

        print(path_egrid)
        print(path_noents)
        egrid_file = read_test_file_2_dict(path_egrid)
        noents_file = read_test_file_2_dict(path_noents)
        print(len(egrid_file))
        print(len(noents_file))
        to_write = combine_files_dict(egrid_file, noents_file, trans)
        write_to_dat(to_write, joined_path)


if __name__ == '__main__':
    main()
