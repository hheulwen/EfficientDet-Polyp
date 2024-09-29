import os
import cv2
import json
import glob
from tqdm import tqdm

fold_id = 3
target_set_name = "train"
target_root_name = os.path.join(r'C:\Users\Chou\CODE\dl_project\kvasir-seg\Kvasir-SEG\train\CV_folds\fold_' + str(fold_id))
source_files_path = os.path.join(
        r'C:\Users\Chou\CODE\dl_project\kvasir-seg\Kvasir-SEG\train\CV_folds\fold_' + str(fold_id),
        target_set_name)
GT_annotation = r'C:\Users\Chou\CODE\dl_project\kvasir-seg\Kvasir-SEG\kavsir_bboxes.json'

print(f"fold: {fold_id} | target: {target_set_name}")
classes = ["polyp"]

os.makedirs(os.path.join(target_root_name, "annotations"), exist_ok=True)
os.makedirs(os.path.join(target_root_name, target_set_name), exist_ok=True)

if os.path.isfile(os.path.join(target_root_name, "annotations", f"instances_{target_set_name}.json")):
    os.remove(os.path.join(target_root_name, "annotations", f"instances_{target_set_name}.json"))

with open(GT_annotation) as f:
    all_annotations = json.load(f)

image_paths = glob.glob(os.path.join(source_files_path, "*.jpg"))
print(f"Found {len(image_paths)} images in {source_files_path}")

annotations = {"categories": [], "images": [], "annotations": []}
for idx, class_name in enumerate(classes):
    annotations["categories"].append({"id": idx + 1, "name": class_name, "supercategory": "None"})

image_counter = 0
annotation_counter = 0

for image_path in tqdm(image_paths):
    image_name = os.path.basename(image_path).split(".")[0]  # Assuming the key in JSON is the image name without extension

    if image_name in all_annotations:
        image_data = all_annotations[image_name]
        bboxes = image_data.get("bbox", [])
        
        try:
            image = cv2.imread(image_path)
            height, width, _ = image.shape

            for bbox in bboxes:
                annotation_dict = {
                    "id": annotation_counter,
                    "image_id": image_counter,
                    "category_id": 1,  # Assuming "polyp" is the only class, adjust if needed
                    "iscrowd": 0,
                    "bbox": [bbox["xmin"], bbox["ymin"], bbox["xmax"] - bbox["xmin"], bbox["ymax"] - bbox["ymin"]],
                    "area": (bbox["xmax"] - bbox["xmin"]) * (bbox["ymax"] - bbox["ymin"])
                }
                annotations["annotations"].append(annotation_dict)
                annotation_counter += 1

            cv2.imwrite(os.path.join(target_root_name, target_set_name, f"{image_counter}.jpg"), image)

            image_dict = {
                "id": image_counter,
                "file_name": f"{image_counter}.jpg",
                "original_file_name": image_name,
                "width": width,
                "height": height
            }
            annotations["images"].append(image_dict)
            image_counter += 1

        except Exception as e:
            print(f"Error processing {image_name}: {str(e)}")
    else:
        print(f"No annotations found for {image_name}")

with open(os.path.join(target_root_name, "annotations", f"instances_{target_set_name}.json"), "w") as outfile:
    json.dump(annotations, outfile)
