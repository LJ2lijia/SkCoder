#!bash

set -eux

DATA="$1"
shift
RUNS="$1"
shift

echo "$@"

mkdir -p runs/cache

for split in train dev test
do  DIR=$RUNS/infer-$split
    mkdir -p $DIR
    python gcb-main.py \
    --do_predict \
    --model_name_or_path $RUNS/test1/checkpoints \
    --run_dir $DIR \
    --output_dir $DIR/checkpoints/ \
    --logging_strategy epoch \
    --cache_dir runs/cache/ \
    --test_file $DATA/${split}_sketcher.json \
    "$@"
    cp $DIR/predictions.txt $DATA/${split}_sketch.jsonl
done
