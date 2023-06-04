#!/usr/bin/env python
from asyncio import Task
from operator import sub
import os
import argparse


def get_cmd(task, sub_task, do_train, model_tag, gpu, data_num, bs, lr, source_length, target_length, patience, epoch, warmup,
            model_dir, summary_dir, res_fn, grad_step, max_steps=None, save_steps=None, log_steps=None):
    if do_train:
        print('============================Start Training==========================')
        cmd_str = 'bash train.sh %s %s %s %s %d %d %d %d %d %d %d %d %s %s %s %d' % \
                  (task, sub_task, model_tag, gpu, data_num, bs, lr, source_length, target_length, patience, epoch,
                   warmup, model_dir, summary_dir, res_fn, grad_step)
    else:
        print('============================Start Inference==========================')
        cmd_str = 'bash inference.sh %s %s %s %s %d %d %d %d %d %d %d %d %s %s %s %d' % \
                  (task, sub_task, model_tag, gpu, data_num, bs, lr, source_length, target_length, patience, epoch,
                   warmup, model_dir, summary_dir, res_fn, grad_step)
    return cmd_str


def get_args_by_task_model(task):
    if task == 'hearthstone':
        src_len = 390
        trg_len = 300
        epoch = 100
        patience = 10
    elif task == 'magic':
        src_len = 640
        trg_len = 768
        epoch = 20
        patience = 5
    elif task == 'AixBench':
        src_len = 512
        trg_len = 512
        epoch = 15
        patience = 3

    if task in ['hearthstone', 'AixBench']:
        bs = 32
    elif task == 'magic':
        bs = 16
    lr = 5
    grad_step = 1

    return bs, lr, src_len, trg_len, patience, epoch, grad_step


def run_one_exp(args):
    bs, lr, src_len, trg_len, patience, epoch, grad_step = get_args_by_task_model(args.task)
    cmd_str = get_cmd(task=args.task, sub_task=args.sub_task, do_train=args.do_train, model_tag=args.model_tag, gpu=args.gpu,
                      data_num=args.data_num, bs=bs, lr=lr, source_length=src_len, target_length=trg_len,
                      patience=patience, epoch=epoch, warmup=3000,
                      model_dir=args.model_dir, summary_dir=args.summary_dir,
                      res_fn='{}/{}_{}.txt'.format(args.res_dir, args.task, args.model_tag), grad_step=grad_step)
    print('%s\n' % cmd_str)
    os.system(cmd_str)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_tag", type=str, default='codet5_base')
    parser.add_argument("--task", type=str, default='hearthstone', choices=['hearthstone', 'magic', 'AixBench'])
    parser.add_argument("--sub_task", type=str, default=None)
    parser.add_argument("--do_train", action='store_true', help='whether to train the model')
    parser.add_argument("--res_dir", type=str, default='results', help='directory to save fine-tuning results')
    parser.add_argument("--model_dir", type=str, default='saved_models', help='directory to save fine-tuned models')
    parser.add_argument("--summary_dir", type=str, default='tensorboard', help='directory to save tensorboard summary')
    parser.add_argument("--data_num", type=int, default=-1, help='number of data instances to use, -1 for full data')
    parser.add_argument("--gpu", type=str, default=0, help='index of the gpu to use in a cluster')
    args = parser.parse_args()

    if not os.path.exists(args.res_dir):
        os.makedirs(args.res_dir)
    run_one_exp(args)


