#!bash

bash ./eval.sh ../data/AixBench-L runs/gcb-aixbench \
    --per_device_eval_batch_size 64 \
    --copy_old_position_embedding False \
    "$@"
