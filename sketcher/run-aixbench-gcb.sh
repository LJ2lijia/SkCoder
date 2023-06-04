NAME=$1
shift

DATA=../data/AixBench-L/
DIR=runs/gcb-aixbench/$NAME

mkdir -p $DIR
mkdir -p runs/cache

TOKENIZERS_PARALLELISM=true \
python gcb-main.py \
--do_train --do_eval --do_predict \
--model_name_or_path microsoft/graphcodebert-base \
--label_all_tokens False \
--run_dir $DIR \
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
--max_seq_length 768 \
--num_train_epochs 10 \
--warmup_ratio 0.1 \
--per_device_train_batch_size 16 \
--per_device_eval_batch_size 32 \
--dataloader_num_workers 16 \
--preprocessing_num_workers 16 \
"$@"
