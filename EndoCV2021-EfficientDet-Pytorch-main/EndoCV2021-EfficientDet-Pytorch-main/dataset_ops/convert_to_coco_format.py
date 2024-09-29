# Created by Gorkem Polat at 10.03.2021
# contact: polatgorkem@gmail.com

import os
import glob
import json
import shutil
import cv2
from tqdm import tqdm

# For single split
target_root_name = os.path.join("../datasets/polyps_all_centers")
target_set_name = "test"
source_files_path = os.path.join("/home/ws2080/Desktop/data/EndoCV2021/edited_files/all_files_test")

classes = ["polyp"]

os.makedirs(target_root_name, exist_ok=True)
os.makedirs(os.path.join(target_root_name, "annotations"), exist_ok=True)

if os.path.isdir(os.path.join(target_root_name, target_set_name)):
    shutil.rmtree(os.path.join(target_root_name, target_set_name))
if os.path.isfile(os.path.join(target_root_name, "annotations", "instances_" + target_set_name + ".json")):
    os.remove(os.path.join(target_root_name, "annotations", "instances_" + target_set_name + ".json"))
os.makedirs(os.path.join(target_root_name, target_set_name))

annotations = {}
annotations["categories"] = []
annotations["images"] = []
annotations["annotations"] = []
for id, class_name in enumerate(classes):
    category = {}
    category["id"] = id + 1
    category["name"] = class_name
    category["supercategory"] = "None"
    annotations["categories"].append(category)

image_paths = glob.glob(os.path.join(source_files_path, "*.jpg"))

image_counter = 0
annotation_counter = 0
for image_path in tqdm(image_paths):
    image_name = image_path.split("/")[-1][:-4]

    with open(image_path[:-4] + ".txt") as f:
        bbox_annotations = f.readlines()

    # eliminate duplicate lines
    bbox_annotations = list(set(bbox_annotations))
    try:
        if len(bbox_annotations) > 0 and not ("\n" in bbox_annotations):
            image = cv2.imread(image_path)
            height, width, _ = image.shape

            for bbox_annotation in bbox_annotations:
                bbox_info = bbox_annotation.split(" ")

                category_id = classes.index(bbox_info[0]) + 1

                x = int(bbox_info[1])
                y = int(bbox_info[2])
                object_width = int(bbox_info[3]) - int(bbox_info[1])
                object_height = int(bbox_info[4]) - int(bbox_info[2])

                annotation_dict = {}
                annotation_dict["id"] = annotation_counter
                annotation_dict["image_id"] = image_counter
                annotation_dict["category_id"] = category_id
                annotation_dict["iscrowd"] = 0
                annotation_dict["area"] = object_width * object_height
                annotation_dict["bbox"] = [x, y, object_width, object_height]
                annotations["annotations"].append(annotation_dict)
                annotation_counter += 1

            cv2.imwrite(os.path.join(target_root_name, target_set_name, str(image_counter) + ".jpg"), image)

            image_dict = {}
            image_dict["id"] = image_counter
            image_dict["file_name"] = str(image_counter) + ".jpg"
            image_dict["original_file_name"] = image_name + ".jpg"
            image_dict["width"] = width
            image_dict["height"] = height
            annotations["images"].append(image_dict)
            image_counter += 1
        else:
            print("No bbox information for: " + image_name)
    except Exception as e:
        print("image path:" + image_path)
        print(str(e.message))
        break

with open(os.path.join(target_root_name, "annotations", "instances_" + target_set_name + ".json"), "w") as outfile:
    json.dump(annotations, outfile)
