#!/usr/bin/env python3.5
# -*- coding: utf-8 -*-
"""
Manually cut out 2 lenslet array image RIOs and
run CNMFe to extract traces.

Created on Jan 29, 2018

@author: izkula
"""
import time

import cosmos.params.dataset_params as params
from cosmos.imaging.frame_processor import FrameProcessor

if __name__ == '__main__':
    ###########################################
    # 1. CHANGE DATA PATHS IN THIS SCRIPT
    # 2. ADD FILENAMES TO cosmos/params/dataset_params.PY
    # 3. CHANGE FLAGS BELOW IN THIS SCRIPT (RUN ONE AT A TIME)
    # 4. CHOOSE VIRTUAL ENV: 'source activate cosmos2'
    # 5. RUN SCRIPT WITHOUT ARGUMENTS
    ##########################################

    # Set the following four flags sequentially

    # This first step requires manual interaction, runs quickly.
    # Will save out to processed_data_dir/date/session_name
    do_select_crop_rois = False

    # Takes a medium amount of time to run.
    # After this runs, verify that
    # processed_data_dir/date/session_name/top/top.tif and
    # .../bot/bot.tif look good (you can load them into ImageJ)
    # to double check that there is no movement and that the video looks good.
    do_process_stacks = False

    # Takes a long time to run.
    do_run_cnmfe = False

    # Requires manual interaction, runs quickly
    do_atlas_align = True

    # The below is going to be dataset specific
    workstation = 'cosmosdata'  # 'cosmosdata', 'analysis2'
    if workstation == 'analysis2':
        raw_data_dir = "/media/optodata/tam/"
        matlab_path = '/home/izkula/Software/Matlab2017b/bin/matlab'
    elif workstation == 'cosmosdata':
        processed_data_dir = "/hdd1/Data/processedData/"
        raw_data_dir = '/home/user/optodata2/tam'
        matlab_path = '/home/user/software/MATLAB/R2018a/bin/matlab'
    print(raw_data_dir, processed_data_dir)

    # Process each dataset
    for i in range(len(params.DATASETS)):
        d = params.DATASETS[i]
        print(d)

        f = FrameProcessor(raw_data_dir=raw_data_dir,
                           processed_data_dir=processed_data_dir,
                           dataset=d)

        # Process both top and bottom ROIs? Or just one
        f.vid_names = ['top', 'bot']

        start = time.time()
        if do_select_crop_rois:
            f.select_crop_rois()
        if do_process_stacks:
            f.crop_stack(
                do_remove_led_frames=True, do_motion_correct=True,
                LED_buffer=4, led_std=1.5)  # generally set led_std=3
            f.plot_motion()
        if do_run_cnmfe:
            f.run_cnmfe(matlab_path, nthreads=6)
        if do_atlas_align:
            f.atlas_align()

        end = time.time()
        print("Elapse time: " + str(end - start))
