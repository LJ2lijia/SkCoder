import json
import fire


def main(data_path=""):
    for prefix in ['train', 'dev', 'test']:
        with open(f'{data_path}/{prefix}_with_sketch.jsonl', 'r') as f_r, open(f'{data_path}/{prefix}_editor.jsonl', 'w') as f_w:
            for line in f_r:
                js = json.loads(line)
                if prefix == 'train':
                    for sketch in js['sketch']:
                        input = ' '.join(js['input_tokens']) + ' [SEP] ' + sketch
                        output = ' '.join(js['output_tokens'])
                        f_w.write(json.dumps({'input': input, 'output': output}) + '\n')
                else:
                    sketch = js['sketch'][0]
                    input = ' '.join(js['input_tokens']) + ' [SEP] ' + sketch
                    output = ' '.join(js['output_tokens'])
                    f_w.write(json.dumps({'input': input, 'output': output}) + '\n')


if __name__ == '__main__':
    fire.Fire(main)
