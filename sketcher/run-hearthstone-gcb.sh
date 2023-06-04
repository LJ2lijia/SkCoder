NAME=$1
shift

DATA=../data/hearthstone
DIR=runs/gcb-hs/$NAME

mkdir -p $DIR
mkdir -p runs/cache

python gcb-main.py \
--do_train --do_eval --do_predict \
--model_name_or_path microsoft/graphcodebert-base \
--label_all_tokens False \
--run_dir $DIR \
--logging_dir $DIR/tensorboard/ \
--logging_strategy epoch \
--save_strategy epoch \
--save_total_limit 5 \
--load_best_model_at_end True \
--metric_for_best_model eval_f1 \
--greater_is_better True \
--evaluation_strategy epoch \
--output_dir $DIR/checkpoints/ \
--cache_dir runs/cache/ \
--train_file $DATA/train_sketcher.json \
--validation_file $DATA/dev_sketcher.json \
--test_file $DATA/test_sketcher.json \
--num_train_epochs 1000 \
--warmup_ratio 0.1 \
--per_device_train_batch_size 32 \
--per_device_eval_batch_size 64 \
"$@"
