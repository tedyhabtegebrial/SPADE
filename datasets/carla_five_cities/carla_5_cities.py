import os
import tqdm
import random
from pathlib import Path

base_path = '/data/teddy/temporary_carla'
dest_path = '/data/teddy/temporary_carla_spade'

towns = [f'Town0{x}' for x in range(1, 6)]
weathers = [f'weather_0{x}' for x in range(4)]
camera_groups_prefix = ['ForwardCameras_', 'SideCameras_', 'HorizontalCameras_']
cams_per_group = [str(x).zfill(2) for x in range(5)]
file_names = [str(x).zfill(6)+'.png' for x in range(0, 10000, 10)]
examples = []
for t in towns:
    for w in weathers:
        for c in camera_groups_prefix:
            for f in file_names:
                c_group = random.choice(cams_per_group)
                examples.append(os.path.join(base_path, t, w, c+c_group, 'rgb', f))
#
label_path = dest_path+'/labels'
images_path = dest_path+'/images'
os.makedirs(label_path, exist_ok=True)
os.makedirs(images_path, exist_ok=True)

def link_file(src_path, dst_path, ):
    os.symlink(src_path, dst_path)

for itr, frame in tqdm.tqdm(enumerate(examples), total=len(examples), unit='images'):
    src_rgb_path = frame
    src_seg_path = src_rgb_path.replace('rgb', 'semantic_segmentation')
    dst_rgb_path = os.path.join(images_path, f'{str(itr).zfill(6)}.png')
    dst_seg_path = os.path.join(label_path, f'{str(itr).zfill(6)}.png')
    os.symlink(src_rgb_path, dst_rgb_path)
    os.symlink(src_seg_path, dst_seg_path)
    # link_file(src_path=src_rgb_path, dst_path=dst_rgb_path)
    # link_file(src_path=src_seg_path, dst_path=dst_seg_path)
