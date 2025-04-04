import os
import json
import numpy as np
import cv2
from glob import glob

# Paths
json_folder = r"D:\MY_PROJECTS\IMAGE_SEGMENT\Images"
output_mask_folder = r"D:\MY_PROJECTS\IMAGE_SEGMENT\NewMask"  # Output directory for masks
output_image_folder = r"D:\MY_PROJECTS\IMAGE_SEGMENT\MaskImages"  # Output directory for original images

# Ensure output directories exist
os.makedirs(output_mask_folder, exist_ok=True)
os.makedirs(output_image_folder, exist_ok=True)

# Get all JSON files
json_files = glob(os.path.join(json_folder, "*.json"))

# Process each JSON file
for json_path in json_files:
    with open(json_path, "r") as f:
        data = json.load(f)
    print("Processing:", json_path)

    # Get image size and path
    image_path = os.path.join(json_folder, data["imagePath"])
    image_width = data["imageWidth"]
    image_height = data["imageHeight"]

    # Read the original image
    original_image = cv2.imread(image_path)
    if original_image is None:
        print(f"Error: Could not read image {image_path}")
        continue

    # Process each shape (label object)
    for i, shape in enumerate(data["shapes"]):
        label = shape["label"]  # Get the label name
        points = np.array(shape["points"], dtype=np.int32)

        # Create a blank mask for the current object
        mask = np.zeros((image_height, image_width), dtype=np.uint8)
        cv2.fillPoly(mask, [points], color=255)  # Fill the polygon with white (255)

        # Save the mask
        mask_filename = os.path.basename(json_path).replace(".json", f"_{label}_mask.png")
        mask_path = os.path.join(output_mask_folder, mask_filename)
        cv2.imwrite(mask_path, mask)

        # Save a copy of the original image with the same name as the mask
        image_filename = os.path.basename(json_path).replace(".json", f"_{label}.png")
        image_path_output = os.path.join(output_image_folder, image_filename)
        cv2.imwrite(image_path_output, original_image)

print("✅ Masks and corresponding images saved in:", output_mask_folder, "and", output_image_folder)