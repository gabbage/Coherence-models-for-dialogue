#!/bin/bash

Corpus="Switchboard"
Tasks="egrid_-coref+noents egrid_-coref egrid_-coref_DAspan egrid_-coref_DAspan_da egrid_-coref_DAspan_da_noentcol simple_egrid_-coref+noents simple_egrid_-coref "
Exp="up hup us ui"

for exp in $Exp; do 
        for task1 in $Tasks; do
                python train_models.py -g $Corpus -m $task1 -s "shuffled_${exp}"
                svm_learn -z p experiments/$Corpus/reordering/$task1/${Corpus}_sal1_range2_2_train.dat "${exp}_${task1}_model"
                #for task2 in $Tasks; do
                        #svm_classify experiments/$Corpus/reordering/$task1/${Corpus}_sal1_range2_2_test.dat "${exp}_${task2}_model" "${task2}_${task1}_prediction"
                
                        #python eval_svmlight_output.py --testfile experiments/$Corpus/reordering/$task/${Corpus}_sal1_range2_2_test.dat --predfile "${task2}_${task1}_prediction" >> logs/$Corpus/$Exp/oot_${task2}_${task1}_result.txt
                #done
        done
done

