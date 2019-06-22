from __future__ import print_function
from __future__ import unicode_literals
from builtins import dict
import os
import csv
import re
import sys
import pandas as pd
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    grids_folder = os.path.join("egrid_-coref/")
    dataset = [x.rstrip('.csv') for x in os.listdir(grids_folder) if x not in ['Params.csv', '.DS_Store.csv']]
    training = [x for x in dataset if x.startswith("train")]
    validation = [x for x in dataset if x.startswith("validation")]
    test = [x for x in dataset if x.startswith("test")]


    splits = pd.DataFrame(dict([(k, pd.Series(v))
                                    for k, v in [('training', training),
                                                 ('validation', validation),
                                                 ('test', test)]]))

    splits.to_csv(path_or_buf="Train_Validation_Test_split.csv")
