# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 17:34:35 2023

@author: zqluo@buaa.edu.cn

MIT Lisence
"""

import os
#import cv2
from imageio.v2 import imread, imsave
import numpy as np
from PIL import Image
#import matplotlib.pyplot as plt
#polar transform
def sample_within_bounds(signal, x, y, bounds):

    xmin, xmax, ymin, ymax = bounds

    idxs = (xmin <= x) & (x < xmax) & (ymin <= y) & (y < ymax)
    
    sample = np.zeros((x.shape[0], x.shape[1], signal.shape[-1]))
    sample[idxs, :] = signal[x[idxs], y[idxs], :]

    return sample

def sample_bilinear(signal, rx, ry):

    signal_dim_x = signal.shape[0]
    signal_dim_y = signal.shape[1]

    # obtain four sample coordinates
    ix0 = rx.astype(int)
    iy0 = ry.astype(int)
    ix1 = ix0 + 1
    iy1 = iy0 + 1

    bounds = (0, signal_dim_x, 0, signal_dim_y)

    # sample signal at each four positions
    signal_00 = sample_within_bounds(signal, ix0, iy0, bounds)
    signal_10 = sample_within_bounds(signal, ix1, iy0, bounds)
    signal_01 = sample_within_bounds(signal, ix0, iy1, bounds)
    signal_11 = sample_within_bounds(signal, ix1, iy1, bounds)

    na = np.newaxis
    # linear interpolation in x-direction
    fx1 = (ix1-rx)[...,na] * signal_00 + (rx-ix0)[...,na] * signal_10
    fx2 = (ix1-rx)[...,na] * signal_01 + (rx-ix0)[...,na] * signal_11

    # linear interpolation in y-direction
    return (iy1 - ry)[...,na] * fx1 + (ry - iy0)[...,na] * fx2

def rev_trans():
    S = 1200 
    height = 832
    width = 1664
    #S=12
    #height = 8
    #width = 16
    i = np.arange(0, S)
    j = np.arange(0, S)
    ii,jj = np.meshgrid(i, j)
    #plt.plot(ii,jj, 'o--')
    #plt.grid(True)
    #plt.show()
    y = height*np.sqrt((ii-S/2.)**2+(jj-S/2.)**2)/(S/1.414)
    x = width/2.*(y/height*np.sin( np.pi/2. *(2*ii-S)/S ))
    #plt.plot(x,y, 'o--')
    #plt.grid(True)
    #plt.show()
    input_dir = '/media/ziqing/S1/ANU_data_test/streetview/'
    output_dir = '/media/ziqing/S1/ANU_data_test/polar/'
    
    images = os.listdir(input_dir)
    for img in images:
        signal = imread(input_dir + img)
        #signal = np.flip(signal , 0)
        image = sample_bilinear(signal, x, y)
        image = image.astype(np.uint8)
        imsave(output_dir + img.replace('jpg','png'), image)

def test_act():
 ###CVACT dataset
    S = 1200
    height = 256
    width = 512

    i = np.arange(0, height)
    j = np.arange(0, width)
    jj, ii = np.meshgrid(j, i)

    y = S/2. - S/2./height*(height-1-ii)*np.sin(2*np.pi*jj/width)
    x = S/2. + S/2./height*(height-1-ii)*np.cos(2*np.pi*jj/width)

    input_dir = '/media/ziqing/S1/ANU_data_test/satview_polish/'
    output_dir = '/media/ziqing/S1/ANU_data_test/polar/'

    if not os.path.exists(input_dir):
        raise NameError("Input-dir don't exist")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        
    images = os.listdir(input_dir)
    le = len(images)
    for index, img in enumerate(images):
        signal = imread(input_dir + img)
        image = sample_bilinear(signal, x, y)
        image = image.astype(np.uint8)
        imsave(output_dir + img.replace('jpg','png'), image)
        if index%100 == 0:
            print('index = ',index, 'total = ',le)
    """for img in images:
        signal = imread(input_dir + img)
        start = int(832 / 4)
        image = signal[start: start + int(832 / 2), :, :]
        #image = cv2.resize(image, (512, 128), interpolation=cv2.INTER_AREA)
        imsave(output_dir + img.replace('.jpg', '.png'), image)"""
        
def resize_img():
    input_dir = 'D:/ANU_data_small/satview_polish/'
    
    output_dir = 'D:/ANU_data_small/streetview_resize/'

    if not os.path.exists(input_dir):
        raise NameError("Input-dir don't exist")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
        
    images = os.listdir(input_dir)
    le = len(images)
    for index, img in enumerate(images):
        signal = imread(input_dir + img)
        #print(signal)
        image = Image.fromarray(signal).resize((512,256))
        #image = image.astype(np.uint8)
        imsave(output_dir + img.replace('jpg','png'), image)
        if index%100 == 0:
            print('index = ',index, 'total = ',le)
        
if __name__ == '__main__':
    test_act()


