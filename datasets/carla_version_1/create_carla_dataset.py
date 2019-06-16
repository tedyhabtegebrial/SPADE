import os
import argparse


#
#This script creates a datasets for SPADE from existing CARLA Dataset.
#"

CARLA_TOWNS = ['Town1', 'Town2']
COLOR_CAMERAS = ['LeftCameraRGB']
SEG_CAMERAS = ['LeftCameraSeg']

TEST_EPISODES = ['Town2/episode_0001', 'Town2/episode_0002']
VAL_EPISODES = ['Town2/episode_0005']

TRAIN_EPISODES =   ['Town1/episode_0000', 'Town1/episode_0001',
                    'Town1/episode_0002','Town1/episode_0003',
                    'Town1/episode_0004','Town1/episode_0005',
                    'Town1/episode_0006','Town1/episode_0007',
                    'Town1/episode_0009','Town1/episode_0011',
                    'Town1/episode_0014',
                    'Town2/episode_0000',
                    'Town2/episode_0003',
                    'Town2/episode_0004',
                    'Town2/episode_0006', 'Town2/episode_0007',
                    'Town2/episode_0009', 'Town2/episode_0011',
                    'Town2/episode_0014']


def check_split(episode):
    ret_type = None
    for name in VAL_EPISODES:
        if name in episode:
            ret_type = 'val'
    for name in TEST_EPISODES:
        if name in episode:
            ret_type = 'test'
    for name in TRAIN_EPISODES:
        if name in episode:
            ret_type = 'train'
    return ret_type
# The rest are used for training

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--source_path',
                type=str, default='/data/teddy/Datasets/carla/temp_carla',
                help='location of the carla dataset')
    arg_parser.add_argument('--destination_path',
                type=str, default='/data/teddy/Datasets/carla/carla_spade',
                help='destination of extracted carla datset suitable for use by SPADE')
    arg_parser.add_argument('--create_links', action='store_true',
                help='Avoids copying data by creating symbolic links ')
    args = arg_parser.parse_args()
    carla_towns = [os.path.join(args.source_path, town) for town in CARLA_TOWNS]
    train_folder = os.path.join(args.destination_path, 'train')
    test_folder = os.path.join(args.destination_path, 'test')
    val_folder = os.path.join(args.destination_path, 'val')
    for folder in [train_folder, val_folder, test_folder]:
        os.makedirs(folder, exist_ok=True)
        os.makedirs(folder+'/labels', exist_ok=True)
        os.makedirs(folder+'/images', exist_ok=True)

    # train episodes, test episode
    for town in carla_towns:
        episodes = [os.path.join(town, e) for e in os.listdir(town)]
        for episode in episodes:
            print(episode)
            episode_type = check_split(episode)
            current_folder = os.path.join(args.destination_path, episode_type)
            curren_img_count = len(os.listdir(current_folder+'/images'))
            # rgb files
            rgb_folder = os.path.join(episode, COLOR_CAMERAS[0])
            seg_folder = os.path.join(episode, SEG_CAMERAS[0])
            rgb_imgs = sorted([os.path.join(rgb_folder, f) for f in os.listdir(rgb_folder)])
            seg_imgs = sorted([os.path.join(seg_folder, f) for f in os.listdir(seg_folder)])
            for i in range(len(rgb_imgs)):
                rgb_dest_name = current_folder + '/images/' + str(curren_img_count+i).zfill(6) + '.png'
                os.symlink(rgb_imgs[i], rgb_dest_name)
                seg_dest_name = current_folder + '/labels/' + str(curren_img_count+i).zfill(6) + '.png'
                os.symlink(seg_imgs[i], seg_dest_name)
    exit()
