from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from pathlib import Path
import json
from tqdm.contrib.concurrent import process_map

def longest_common_subsequence(x: list, y: list):
  """
  Finds the longest common subsequence between two strings. Also returns the
  The subsequence found
  Parameters
  ----------
  x: list, one string
  y: list, the other string
  Returns
  -------
  Matches: list, the index of selected tokens in y
  >>> longest_common_subsequence("programming", "gaming")
  [0, 1, 2, 3, 4, 5]
  >>> longest_common_subsequence("physics", "smartphone")
  [5, 6]
  >>> longest_common_subsequence("computer", "food")
  [1] or [2]
  """
  m = len(x)
  n = len(y)

  # declaring the array for storing the dp values
  L = [[None] * (n + 1) for _ in range(m + 1)]
  for i in range(0, m + 1):
    L[i][0] = 0
  for j in range(0, n + 1):
    L[0][j] = 0

  for i in range(1, m + 1):
    for j in range(1, n + 1):
      if x[i - 1] == y[j - 1]:
        match = 1
      else:
        match = 0

      L[i][j] = max(L[i - 1][j], L[i][j - 1], L[i - 1][j - 1] + match)

  matches = []
  i, j = m, n
  while i > 0 and j > 0:
    if x[i - 1] == y[j - 1]:
      match = 1
    else:
      match = 0

    if L[i][j] == L[i - 1][j - 1] + match:
      if match == 1:
        matches = [j - 1] + matches
      i -= 1
      j -= 1
    elif L[i][j] == L[i - 1][j]:
      i -= 1
    else:
      j -= 1

  return matches

def common_tokens(code, example):
  return [i for i, token in enumerate(example) if token in set(code)]

def get_parser():
  parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
  parser.add_argument('--input', type=str, required=True)
  parser.add_argument('--output', type=str, required=False, default=None)
  parser.add_argument('--nl', type=str, default='input_tokens')
  parser.add_argument('--code', type=str, default='output_tokens')
  parser.add_argument('--example', type=str, default='examples')
  parser.add_argument('--nl_length', type=int, default=None)
  parser.add_argument('--code_length', type=int, default=None)
  parser.add_argument('--num_workers', type=int, default=None)
  parser.add_argument('--use_common_tokens', action='store_true')
  parser.add_argument('--tokenize_nl', action='store_true')
  parser.add_argument('--tokenize_code', action='store_true')
  return parser

def process_line(line):
  j, sample = line
  sample = json.loads(sample)
  if args.tokenize_nl:
    sample[args.nl] = sample[args.nl].split()
  if args.tokenize_code:
    sample[args.code] = sample[args.code].split()
  code = sample[args.code] if args.code in sample and sample[args.code] else sample[args.example][0].split()
  for token in code + sample[args.nl]:
    assert ' ' not in token
  lines = []
  if args.example not in sample:
    return lines
  for i, example in enumerate(sample[args.example]):
    example = example.split()
    sketch_function = common_tokens if args.use_common_tokens else longest_common_subsequence
    indices = sketch_function(code, example)
    for token in example:
      assert ' ' not in token
    lines.append(json.dumps(dict(
      intent=' '.join(sample[args.nl][:args.nl_length]),
      example=' '.join(example[:args.code_length]),
      tag=[int(k in indices) for k in range(len(example))][:args.code_length],
      source=f'sample{j}-example{i}'
    )))
  return lines


def main(args):
  input = Path(args.input)
  assert input.exists() and input.is_file()
  if args.output is None:
    output = input.with_name(input.stem + '.output' + input.suffix)
  else:
    output = Path(args.output)
  inputs = list(enumerate(input.open().readlines()))
  process_dict = {}
  if args.num_workers:
    process_dict['max_workers'] = args.num_workers
  lines = process_map(process_line, inputs, chunksize=1, **process_dict)
  with output.open('w') as output:
    for line_group in lines:
      for line in line_group:
        print(line, file=output)

if __name__ == '__main__':
  parser = get_parser()
  args = parser.parse_args()
  main(args)
  
