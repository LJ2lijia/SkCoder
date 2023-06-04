#!bash

bash ./eval.sh ../data/magic runs/gcb-mtg \
    --max_seq_length 768 \
    --copy_old_position_embedding False \
    --per_device_eval_batch_size 64 \
    "$@"
