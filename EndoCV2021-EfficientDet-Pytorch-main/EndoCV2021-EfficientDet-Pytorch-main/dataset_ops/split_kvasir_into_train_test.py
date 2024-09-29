# Created by Gorkem Polat at 15.03.2021
# contact: polatgorkem@gmail.com

import os
import glob
import shutil
import random

all_images_path = r'C:\Users\Chou\CODE\dl_project\kvasir-seg\Kvasir-SEG\images'
train_folder = r'C:\Users\Chou\CODE\dl_project\kvasir-seg\Kvasir-SEG\train'
test_folder = r'C:\Users\Chou\CODE\dl_project\kvasir-seg\Kvasir-SEG\test'
test_ratio = 0.2

if os.path.isdir(train_folder):
    shutil.rmtree(train_folder)
os.mkdir(train_folder)

if os.path.isdir(test_folder):
    shutil.rmtree(test_folder)
os.mkdir(test_folder)

images = glob.glob(os.path.join(all_images_path, "*.jpg"))
random.shuffle(images)

test_images = images[:int(len(images) * test_ratio)]
train_images = images[int(len(images) * test_ratio):]

for test_image in test_images:
    file_name = os.path.basename(test_image)
    mask_name = file_name.replace(".jpg", ".png")
    
    # Check if image already exists in test_folder
    if not os.path.exists(os.path.join(test_folder, 'images', file_name)):
        shutil.copyfile(test_image, os.path.join(test_folder, 'images', file_name))
    
    # Check if mask already exists in test_folder
    if os.path.exists(os.path.join(all_masks_path, mask_name)):
        shutil.copyfile(os.path.join(all_masks_path, mask_name), os.path.join(test_folder, 'masks', mask_name))

for train_image in train_images:
    file_name = os.path.basename(train_image)
    mask_name = file_name.replace(".jpg", ".png")
    
    # Check if image already exists in train_folder
    if not os.path.exists(os.path.join(train_folder, 'images', file_name)):
        shutil.copyfile(train_image, os.path.join(train_folder, 'images', file_name))
    
    # Check if mask already exists in train_folder
    if os.path.exists(os.path.join(all_masks_path, mask_name)):
        shutil.copyfile(os.path.join(all_masks_path, mask_name), os.path.join(train_folder, 'masks', mask_name))