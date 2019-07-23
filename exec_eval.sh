#!/bin/bash

Corpus="Switchboard"
Tasks="egrid_-coref+noents egrid_-coref egrid_-coref_DAspan egrid_-coref_DAspan_da egrid_-coref_DAspan_da_noentcol simple_egrid_-coref+noents simple_egrid_-coref"
Exp="hup"

for task in $Tasks; do
        echo $task
        #python generate_grid.py DailyDialog $task $task data/
        #python generate_shuffled.py -gs DailyDialog -m $task
        
        python train_models.py -g $Corpus -m $task -s "shuffled_${Exp}"

        svm_learn -z p experiments/$Corpus/reordering/$task/${Corpus}_sal1_range2_2_train.dat "${task}_model"
        svm_classify experiments/$Corpus/reordering/$task/${Corpus}_sal1_range2_2_test.dat "${task}_model" "${task}_prediction"
        
        python eval_svmlight_output.py --testfile experiments/$Corpus/reordering/$task/${Corpus}_sal1_range2_2_test.dat --predfile "${task}_prediction" >> logs/$Corpus/$Exp/${task}_result.txt
done

CombTasks="egrid_-coref simple_egrid_-coref"
for task in $CombTasks; do
        echo "combining ${task}"
        python generate_joined_dat.py -g $Corpus -m1 $task
done

