#!bash

bash ./eval.sh ../data/hearthstone runs/gcb-hs \
    --per_device_eval_batch_size 256 \
    "$@"
