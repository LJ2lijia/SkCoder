import json
import fire


def preprocess(data_path):
    for prefix in ['train', 'dev', 'test']:
        with open(f'{data_path}/{prefix}.jsonl', 'r') as f_r, open(f'{data_path}/{prefix}.in', 'w') as f_w:
            for line in f_r:
                sample = json.loads(line.strip())
                f_w.write(' '.join(sample['input_tokens'])+'\n')


def postprocess(data_path, example_path):
    retrieval_corpus = []
    with open(f'{data_path}/train.jsonl', 'r') as f:
        for line in f:
            sample = json.loads(line.strip())
            retrieval_corpus.append(sample)

    for prefix in ['train', 'dev', 'test']:
        with open(f'{example_path}/{prefix}.example', 'r') as f_ex, open(f'{data_path}/{prefix}.jsonl', 'r') as f_data:
            with open(f'{data_path}/{prefix}_with_example.jsonl', 'w') as f_w:
                f_ex = f_ex.readlines()
                f_data = f_data.readlines()
                assert len(f_ex) == len(f_data)
                for line_ex, line_data in zip(f_ex, f_data):
                    example_ids = line_ex.strip().split()
                    sample = json.loads(line_data.strip())
                    target_code = ' '.join(sample['output_tokens'])
                    examples = []
                    for idx in example_ids:
                        retrieved_code = retrieval_corpus[int(idx)]['output_tokens']
                        retrieved_code = ' '.join(retrieved_code)
                        if retrieved_code == target_code: # remove target code
                            continue
                        elif len(examples) >= 5: # only keep top-5 examples
                            break
                        else:
                            examples.append(retrieved_code)            
                    sample['examples'] = examples
                    f_w.write(json.dumps(sample)+'\n')


def main(type="", data_path="", example_path=""):
    if type == 'preprocess':
        preprocess(data_path)
    elif type == 'postprocess':
        postprocess(data_path, example_path)


if __name__ == '__main__':
    fire.Fire(main)