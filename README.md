# SkCoder: A Sketch-based Approach for Automatic Code Generation

Official implementation of our ICSE 2023 paper on Automatic Code Generation. [Paper](https://arxiv.org/abs/2302.06144)

## Table of Contents

- Requirements
- Datasets
- Usage
- Releasing a trained model
- Acknowledgement
- Citation

## Requirements

- Java 1.8.0
- python 3.10
- pytorch 1.13.1
- transformers 4.24.0
- tqdm 4.60.0
- tree_sitter 0.2.0
- fire 0.5.0
- nltk
- tensorboard

## Datasets

In this paper, we conduct experiments on three datasets, including `HearthStone`, `Magic`, and `AixBench-L`. The raw datasets are available at [Google Drive](https://drive.google.com/drive/folders/1p04arpnmGT_QdeG_v5I-OkGj517wHXGI?usp=drive_link).

Please download the datasets and put them in the `data` folder. Taking the `HearthStone` dataset as an example, the folder structure should be like this:

```
data
├── hearthstone
│   ├── train.jsonl
│   ├── dev.jsonl
│   ├── test.jsonl
│   ├── train_with_example.jsonl
│   ├── dev_with_example.jsonl
│   ├── test_with_example.jsonl
```

Each line of these `jsonl` files is a json object, which contains the following fields:

- input: str, the original input
- input_tokens[list]: list[str], the tokenized input
- output: str, the original output
- output_tokens[list]: list[str], the tokenized output


## Usage

### Step 1: Runing the Retriever

The retriever is used to retrieve the most similar code snippets from the code corpus. We also provide the retrieval results for the three datasets, which can be downloaded from [Google Drive](https://drive.google.com/drive/folders/1p04arpnmGT_QdeG_v5I-OkGj517wHXGI?usp=drive_link). You can skip this step if you want to use the retrieval results directly.


We run the retriever on the `HearthStone` dataset as an example.
First, we extract input requirements from datasets and save them as files (`train.in`, `dev.in`, `test.in`).

```Bash
python process4retriever.py \
    --type preprocess \
    --data_path data/hearthstone \
```

Then, we utilze a search engine to retrieve similar code snippets from the train data.

```Bash
cd retriever
bash compile.sh
bash buildIndex.sh
bash buildExemplars.sh
```

Next, we extract similar code snippets and save them as `jsonl` files into `data/hearthstone`, including `{train, dev, test}_with_example.jsonl`.
Each file contains the following keys:

- input: str, the original input
- input_tokens[list]: list[str], the tokenized input
- output: str, the original output
- output_tokens[list]: list[str], the tokenized output
- examples: list[str], the Top-K similar code snippets

### Step 2: Training the Sketcher

As an example, we show the preprocessing, training and inference process of HearthStone dataset.

There are some details that are different for each dataset, but mostly the steps are the same. We will add the details later.

As a disclaimer, the term `gcb` appearing everywhere stands for GraphCodeBert, which we use as a base model for fine-tuning.
It is here because there was a version that trains the model from scratch, so the term gcb is thus used to distinguish them.

#### Data Preprocessing

Run preprocess.py on the `{train,dev,test}_with_example.jsonl` to produce `{train,valid,test}_sketcher.json`.

```Bash
cd sketcher
python preprocess.py --input ../data/hearthstone/train_with_example.jsonl --output ../data/hearthstone/train_sketcher.json
python preprocess.py --input ../data/hearthstone/dev_with_example.jsonl --output ../data/hearthstone/dev_sketcher.json
python preprocess.py --input ../data/hearthstone/test_with_example.jsonl --output ../data/hearthstone/test_sketcher.json
```

#### Training
Run `run-hearthstone-gcb.sh`.
```Bash
export CUDA_VISIBLE_DEVICES=0 # the GPU(s) you want to use to train
bash run-hearthstone-gcb.sh test1
```
`test1` is the default `runs` folder used for the run. If you changed the folder name, you should change corresponding path in `eval.sh`.

#### Generating data for the editor
First run the inference script with the GPU.
```bash
export CUDA_VISIBLE_DEVICES=0 # the GPU(s) you want to use to inference
bash eval-hearthstone-gcb.sh
```
Then run `add_sketch.py` with the data folder path as the parameter to generate `{train,dev,test}_with_sketch.jsonl`.
```Bash
python add_sketch.py --data ../data/hearthstone
```

Finally, the sketcher outputs `{train,dev,test}_with_sketch.jsonl` in `data/hearthstone`. The format of these files is the same as the input of the retriever, except two more columns:

- sketch: a list of sketch from each example, where each sketch is a string. Note that we use <pad> instead of [PAD] .
- oracle-sketch: a list of oracle sketches for each example. The format is the same as sketch.

### Step 3: Training the Editor

The editor is train to generate code based on the requirement and code sketch. We run the editor on the `HearthStone` dataset as an example.

#### Data Preprocessing
We run `process2editor.py` to generate the training data for the editor.

```Bash
python process4editor.py --data_path data/hearthstone
```

The generated data is saved in `data/hearthstone/{train,dev,test}_editor.jsonl`.

#### Training and Inference
Please modify the `ROOT_DIR` in `train.sh` and `inference.sh`, which denote the absolute path of the project.
```Bash
cd editor/sh
python run_exp.py --do_train --task hearthstone --gpu {gpu_ids}
```
Where `gpu_ids` is the GPU(s) you want to use to train, such as `0,1`.

`run_exp.py` will automatically train the model and generate the code for the test data. The generated code is saved in `editor/sh/saved_models/hearthstone/prediction/test_best-bleu.jsonl`. 

### Step 4: Evaluation
We evaluate the generated code using three metrics, including Exact Match (EM), BLEU, and CodeBLEU. We run the evaluation on the `HearthStone` dataset as an example.

```Bash
cd evaluator
python evaluator.py --input_file {prediction_path} --lang {lang}
```

Where `prediction_path` is the path of the generated code, such as `../editor/sh/saved_models/hearthstone/prediction/test_best-bleu.jsonl`.
`lang` is the programming language of the generated code (`Hearthstone`: `python`, `Magic` and `AixBench-L`: `java`).


## Releasing a trained model
To facilitate the research community, we release the trained checkpoints of the sketcher and editor. The models are available at Google Drive([Sketcher](https://drive.google.com/drive/folders/1Vo48FC-pfX3FJwJihef6w2KWW-vjnu9B?usp=drive_link), [Editor](https://drive.google.com/drive/folders/17irATOV2xvle7Dq20-qydQDtV49PaG3C?usp=drive_link)). Please download the models and put them in the corresponding folders. Take the HearthStone dataset as an example, the folder structure is as follows:

```
sketcher
├── runs
│   ├── gcb-hs
```


```
editor
├── sh
│   ├── saved_models
│   │   ├── hearthstone
```

Then, you can run the inference script to generate the code for the test data.

```Bash
cd editor/sh
python run_exp.py --task hearthstone --gpu {gpu_ids}
```


## Acknowledgement
The code is based on [Re2Com](https://github.com/Gompyn/re2com-opensource), [GraphCodeBERT](https://github.com/microsoft/CodeBERT/tree/master/GraphCodeBERT), and [CodeT5](https://github.com/salesforce/CodeT5). We thank the authors for their great work.

## Citation
If you find this repository useful, please cite our paper:
```
@inproceedings{SkCoder,
  title={SkCoder: A Sketch-based Approach for Automatic Code Generation},
  author={Li, Jia and Li, Yongmin and Li, Ge and Jin, Zhi and Hao, Yiyang and Hu, Xing},
  booktitle={Proceedings of the ACM/IEEE 45nd International Conference on Software Engineering},
  year={2023}
}
```
