python3.6 ../train.py --name spade_on_carla_five_cities --dataset_mode custom \
      --use_vae --label_dir /data/teddy/temporary_carla_spade/label_path --image_dir \
      /data/teddy/temporary_carla_spade/images --label_dir /data/teddy/temporary_carla_spade/labels \
      --gpu_ids 4,5,6,7 --label_nc 13 --no_instance --batchSize 8 \
      --checkpoints_dir /home/habtegebrial/experiments_eccv --load_size 256 --crop_size 256
