"""
# -*- coding: utf-8 -*-
-----------------------------------------------------------------------------------
# Author: Nguyen Mau Dung
# DoC: 2020.05.21
# email: nguyenmaudung93.kstn@gmail.com
# project repo: https://github.com/maudzung/TTNet-Realtime-for-Table-Tennis-Pytorch
-----------------------------------------------------------------------------------
# Description: The configurations of the project will be defined here
"""

import torch
import os
import datetime
import argparse #命令行接口 
from easydict import EasyDict as edict
import sys

sys.path.append('../')

from utils.misc import make_folder


def parse_configs(arg):
    configs = edict()
    configs.seed= 2020
    configs.saved_fn='ttnet'
    ####################################################################
    ##############     Model configs            ###################
    ####################################################################
    configs.arch='ttnet'
    configs.dropout_p=0.5
    configs.multitask_learning=False
    configs.no_local=False
    configs.no_event=False
    configs.no_seg=False
    configs.pretrained_path=None
    configs.overwrite_global_2_local=False

    ####################################################################
    ##############     Dataloader and Running configs            #######
    ####################################################################
    # parser.add_argument('--working-dir', type=str, default='..\\..\\', metavar='PATH',
    #                     help='the ROOT working directory')
    # 暂时用绝对路径 
    configs.working_dir='E:\\w\\bs\\c\\TTNet-Real-time-Analysis-System-for-Table-Tennis-Pytorch-master/src'
    configs.no_val=False
    configs.no_test=False
    configs.no_size=0.2
    configs.smooth_labelling=False
    configs.num_samples=None
    configs.num_workers=4
    configs.batch_size=8
    configs.print_freq=50
    configs.checkpoint_freq=2
    configs.sigma=1.
    configs.thresh_ball_pos_mask=0.05
    ####################################################################
    ##############     Training strategy            ###################
    ####################################################################
    configs.start_epoch=1
    configs.num_epochs=30
    configs.lr=1e-3
    configs.minimum_lr=1e-7
    configs.momentum=0.9
    configs.weight_decay=0
    configs.optimizer_type='adam'
    configs.lr_type='plateau'
    configs.lr_factor=0.5
    configs.lr_step_size=5
    configs.lr_patience=3
    configs.earlystop_patience=None
    configs.freeze_global=False
    configs.freeze_local=False
    configs.freeze_event=False
    configs.freeze_seg=False

    ####################################################################
    ##############     Loss weight            ###################
    ####################################################################
    configs.bce_weight=0.5
    configs.global_weight=1.
    configs.local_weight=1.
    configs.event_weight=1.
    configs.seg_weight=1.

    ####################################################################
    ##############     Distributed Data Parallel            ############
    ####################################################################
    configs.world_size=-1
    configs.rank=-1
    configs.dist_url='tcp://127.0.0.1:29500'
    configs.dist_backend='nccl'
    configs.gpu_idx=None
    configs.no_cuda=False
    configs.multiprocessing_distributed=False

    ####################################################################
    ##############     Evaluation configurations     ###################
    ####################################################################
    configs.evaluate=False
    configs.resume_path=None
    configs.use_best_checkpoint=False
    configs.seg_thresh=0.5
    configs.event_thresh=0.5
    configs.save_test_output=False

    ####################################################################
    ##############     Demonstration configurations     ###################
    ####################################################################
    configs.video_path=None
    configs.output_format='text'
    configs.show_image=False
    configs.save_demo_output=False


    configs.update(arg)

    ####################################################################
    ############## Hardware configurations ############################
    ####################################################################
    configs.device = torch.device('cpu' if configs.no_cuda else 'cuda')
    configs.ngpus_per_node = torch.cuda.device_count()

    configs.pin_memory = True

    ####################################################################
    ##############     Data configs            ###################
    ####################################################################
    configs.dataset_dir = os.path.join(configs.working_dir, 'dataset')
    configs.train_game_list = ['game_1', 'game_2', 'game_3', 'game_4', 'game_5']
    configs.test_game_list = ['test_1', 'test_2', 'test_3', 'test_4', 'test_5', 'test_6', 'test_7']
    configs.events_dict = {
        'bounce': 0,
        'net': 1,
        'empty_event': 2
    }
    configs.events_weights_loss_dict = {
        'bounce': 1.,
        'net': 3.,
    }
    configs.events_weights_loss = (configs.events_weights_loss_dict['bounce'], configs.events_weights_loss_dict['net'])
    configs.num_events = len(configs.events_weights_loss_dict)  # Just "bounce" and "net hits"
    configs.num_frames_sequence = 9

    configs.org_size = (1920, 1080)
    configs.input_size = (320, 128)

    configs.tasks = ['global', 'local', 'event', 'seg']
    if configs.no_local:
        if 'local' in configs.tasks:
            configs.tasks.remove('local')
        if 'event' in configs.tasks:
            configs.tasks.remove('event')
    if configs.no_event:
        if 'event' in configs.tasks:
            configs.tasks.remove('event')
    if configs.no_seg:
        if 'seg' in configs.tasks:
            configs.tasks.remove('seg')

    # Compose loss weight for tasks, normalize the weights later
    loss_weight_dict = {
        'global': configs.global_weight,
        'local': configs.local_weight,
        'event': configs.event_weight,
        'seg': configs.seg_weight
    }
    configs.tasks_loss_weight = [loss_weight_dict[task] for task in configs.tasks]

    configs.freeze_modules_list = []
    if configs.freeze_global:
        configs.freeze_modules_list.append('ball_global_stage')
    if configs.freeze_local:
        configs.freeze_modules_list.append('ball_local_stage')
    if configs.freeze_event:
        configs.freeze_modules_list.append('events_spotting')
    if configs.freeze_seg:
        configs.freeze_modules_list.append('segmentation')

    ####################################################################
    ############## logs, Checkpoints, and results dir ########################
    ####################################################################
    configs.checkpoints_dir = os.path.join(configs.working_dir, 'checkpoints', configs.saved_fn)
    configs.logs_dir = os.path.join(configs.working_dir, 'logs', configs.saved_fn)
    configs.use_best_checkpoint = True

    if configs.use_best_checkpoint:
        configs.saved_weight_name = os.path.join(configs.checkpoints_dir, '{}_best.pth'.format(configs.saved_fn))
    else:
        configs.saved_weight_name = os.path.join(configs.checkpoints_dir, '{}.pth'.format(configs.saved_fn))

    configs.results_dir = os.path.join(configs.working_dir, 'results')

    make_folder(configs.checkpoints_dir)
    make_folder(configs.logs_dir)
    make_folder(configs.results_dir)

    if configs.save_test_output:
        configs.saved_dir = os.path.join(configs.results_dir, configs.saved_fn)
        make_folder(configs.saved_dir)

    if configs.save_demo_output:
        configs.save_demo_dir = os.path.join(configs.results_dir, 'demo', configs.saved_fn)
        make_folder(configs.save_demo_dir)

    return configs


if __name__ == "__main__":
    configs = parse_configs()

    print(datetime.date.today())
    print(datetime.datetime.now().year)
