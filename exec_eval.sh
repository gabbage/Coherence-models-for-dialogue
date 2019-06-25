#!/bin/bash

Tasks="egrid_-coref simple_egrid_-coref egrid_-coref_DAspan egrid_-coref_DAspan_da egrid_-coref_DAspan_da_noentcol" # extgrid_-coref

for task in $Tasks; do
        echo $task
        #python generate_grid.py DailyDialog $task $task data/
        python generate_shuffled.py -gs DailyDialog -m $task
        
        python train_models.py -g DailyDialog -m $task
        svm_learn -z p experiments/DailyDialog/reordering/$task/DailyDialog_sal1_range2_2_train.dat
        svm_classify experiments/Oasis/reordering/$task/DailyDialog_sal1_range2_2_test.dat "${test}_model" "${test}_prediction"
        
        python eval_svmlight_output.py --testfile experiments/DailyDialog/reordering/$task/DailyDialog_sal1_range2_2_test.dat --predfile "${test}_prediction"
done
