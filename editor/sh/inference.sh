ROOT_DIR="/home/xxx/SkCoder"
WORKDIR=${ROOT_DIR}/editor
export PYTHONPATH=$WORKDIR

TASK=${1}
SUB_TASK=${2}
MODEL_TAG=${3}
GPU=${4}
DATA_NUM=${5}
BS=${6}
LR=${7}
SRC_LEN=${8}
TRG_LEN=${9}
PATIENCE=${10}
EPOCH=${11}
WARMUP=${12}
MODEL_DIR=${13}
SUMMARY_DIR=${14}
RES_FN=${15}
GRAD_STEP=${16}

if [[ $DATA_NUM == -1 ]]; then
  DATA_TAG='all'
else
  DATA_TAG=$DATA_NUM
  EPOCH=1
fi

OUTPUT_DIR=${MODEL_DIR}/${TASK}
CACHE_DIR=${OUTPUT_DIR}/cache_data
RES_DIR=${OUTPUT_DIR}/prediction
LOG=${OUTPUT_DIR}/train.log
mkdir -p ${OUTPUT_DIR}
mkdir -p ${CACHE_DIR}
mkdir -p ${RES_DIR}

MODEL_TYPE=codet5
TOKENIZER=Salesforce/codet5-base
MODEL_PATH=Salesforce/codet5-base
RUN_FN=${WORKDIR}/run_gen.py


CUDA_VISIBLE_DEVICES=${GPU} \
  python ${RUN_FN}  ${MULTI_TASK_AUG}   \
  --do_test \
  --task ${TASK} --sub_task ${SUB_TASK} --model_type ${MODEL_TYPE} --data_num ${DATA_NUM}  \
  --num_train_epochs ${EPOCH} --warmup_steps ${WARMUP} --learning_rate ${LR}e-5 --patience ${PATIENCE} \
  --tokenizer_name=${TOKENIZER}  --model_name_or_path=${MODEL_PATH} --data_dir ${ROOT_DIR}/data  \
  --cache_path ${CACHE_DIR}  --output_dir ${OUTPUT_DIR}  --summary_dir ${SUMMARY_DIR} \
  --save_last_checkpoints --always_save_model --res_dir ${RES_DIR} --res_fn ${RES_FN} \
  --gradient_accumulation_steps ${GRAD_STEP} \
  --train_batch_size ${BS} --eval_batch_size ${BS} --max_source_length ${SRC_LEN} --max_target_length ${TRG_LEN} \
  2>&1 | tee ${LOG}