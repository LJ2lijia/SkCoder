import json
import argparse
from pathlib import Path

LIST = ['train', 'dev', 'test']
def process(tokens, tags):
  tokens = tokens.split()
  assert len(tokens) >= len(tags)
  PAD = '<pad>'
  def gen_sketch():
    last = None
    for token, tag in zip(tokens, tags):
      if tag == 1:
        last = token
        yield token
      else:
        if last != PAD:
          yield PAD
        last = PAD
  ret = list(gen_sketch())
  # if len(tokens) > len(tags):
  #   print('truncated!')
  #   ret += [(a, 'truncated') for a in tokens[len(tags):]]
  return ' '.join(ret)

def get_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('--data', type=Path, required=True)
  return parser

def main(args):
  # data = args.data
  assert args.data.exists() and args.data.is_dir()
  for part in LIST:
    print(part)
    sketch = iter([json.loads(line) for line in open(args.data / f'{part}_sketch.jsonl')])
    oracle = iter([json.loads(line)['tag'] for line in open(args.data / f'{part}_sketcher.json')])
    data = [json.loads(line) for line in open(args.data / f'{part}_with_example.jsonl')]
    for sample in data:
      if 'examples' not in sample:
        continue
      sample['sketch'] = [process(example, next(sketch)) for example in sample['examples']]
      sample['oracle-sketch'] = [process(example, next(oracle)) for example in sample['examples']]
    with open(args.data / f'{part}_with_sketch.jsonl', 'w') as f:
      for line_i in data:
        print(json.dumps(line_i), file=f)

if __name__ == '__main__':
  args = get_parser().parse_args()
  main(args)
