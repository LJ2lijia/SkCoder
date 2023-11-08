import json
import nltk
from CodeBLEU import calc_code_bleu
from bleu_score import compute_bleu
import fire

work_dir = "/home/xxx/SkCoder/editor/sh/saved_models"

def main(input_file, lang):
    em, total_num = 0, 0
    bleu = 0.0
    predictions, references = [], []
    with open(input_file, 'r') as f:
        for line in f:
            js = json.loads(line)
            pred = js['prediction']
            refer = js['target']
            if pred == refer:
                em += 1
            try:
                bleu += nltk.translate.bleu_score.sentence_bleu([refer.split()], pred.split())
            except:
                print(refer)
                print(pred)
            total_num += 1
            predictions.append(pred)
            references.append(refer)

    codebleu = calc_code_bleu.get_codebleu([references], predictions, lang)

    print('EM: {0}, BLEU: {1}, CodeBLEU: {2}'.format(em / total_num, bleu / total_num, codebleu))


if __name__ == '__main__':
    fire.Fire(main)
