import os
import json
import numpy as np
import cv2
from glob import glob


# Path to the JSON file
json_folder = r"D:\MY_PROJECTS\IMAGE_SEGMENT\Images"
output_mask_folder = r"D:\MY_PROJECTS\IMAGE_SEGMENT\Mask"  # Output directory for masks

# Ensure output directory exists
os.makedirs(output_mask_folder, exist_ok=True)

# Get all JSON files
json_files = glob(os.path.join(json_folder, "*.json"))

# Process each JSON file
for json_path in json_files:
    with open(json_path, "r") as f:
        data = json.load(f)
    print("Processing:", json_path)
    # Get image size
    image_width = data["imageWidth"]
    image_height = data["imageHeight"]

    # Create blank mask (grayscale)
    mask = np.zeros((image_height, image_width), dtype=np.uint8)

    # Process each shape (L-bent object)
    for i, shape in enumerate(data["shapes"]):
        points = np.array(shape["points"], dtype=np.int32)
        cv2.fillPoly(mask, [points], color=i*20+20)  # Assign unique grayscale ID

    # Save the mask
    mask_filename = os.path.basename(json_path).replace(".json", "_mask.png")
    mask_path = os.path.join(output_mask_folder, mask_filename)
    cv2.imwrite(mask_path, mask)
    

print("✅ Masks saved in:", output_mask_folder)


##########################################################
