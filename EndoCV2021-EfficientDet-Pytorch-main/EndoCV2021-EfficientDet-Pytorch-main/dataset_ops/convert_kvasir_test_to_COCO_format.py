import os
import glob
import cv2
import json
from tqdm import tqdm

target_set_name = "images"
source_files_path = os.path.join(
    r'C:\Users\Chou\CODE\dl_project\kvasir-seg\Kvasir-SEG\test', target_set_name)
GT_annotation = r'C:\Users\Chou\CODE\dl_project\kvasir-seg\Kvasir-SEG\kavsir_bboxes.json'

classes = ["polyp"]

# Load the custom JSON annotations
with open(GT_annotation) as f:
    all_annotations = json.load(f)

# Gather all images
image_paths = glob.glob(os.path.join(source_files_path, "*.jpg"))
print(f"Found {len(image_paths)} images in {source_files_path}")

annotations = {
    "categories": [],
    "images": [],
    "annotations": []
}

# Create categories
for id, class_name in enumerate(classes):
    category = {
        "id": id + 1,
        "name": class_name,
        "supercategory": "None"
    }
    annotations["categories"].append(category)

image_counter = 0
annotation_counter = 0

# Iterate through all image paths
for image_path in tqdm(image_paths):
    image_name = os.path.basename(image_path)  # Use os.path.basename to get the filename
    print("Processing image:", image_name)

    # Check if image_name exists in all_annotations
    if image_name.split('.')[0] not in all_annotations:
        print("No matching image ID found for:", image_name)
        continue  # Skip this image if no ID is found

    image_data = all_annotations[image_name.split('.')[0]]  # Get the image's data
    height = image_data["height"]
    width = image_data["width"]

    # Prepare the image dict
    image_dict = {
        "id": image_counter,
        "file_name": image_name,
        "width": width,
        "height": height
    }
    annotations["images"].append(image_dict)

    # Process the bounding boxes
    for bbox in image_data["bbox"]:
        annotation_dict = {
            "id": annotation_counter,
            "image_id": image_counter,
            "category_id": 1,  # Assuming "polyp" is category_id 1
            "iscrowd": 0,
            "area": (bbox["xmax"] - bbox["xmin"]) * (bbox["ymax"] - bbox["ymin"]),
            "bbox": [
                bbox["xmin"],
                bbox["ymin"],
                bbox["xmax"] - bbox["xmin"],
                bbox["ymax"] - bbox["ymin"]
            ]
        }
        annotations["annotations"].append(annotation_dict)
        annotation_counter += 1

    image_counter += 1

# Save the annotations to a JSON file
output_path = r'C:\Users\Chou\CODE\dl_project\kvasir-seg\Kvasir-SEG\kavsir_bboxes_coco_format.json'
with open(output_path, "w") as outfile:
    json.dump(annotations, outfile)

print(f"Annotations saved to {output_path}")
