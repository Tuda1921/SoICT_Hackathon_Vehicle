from ultralytics import RTDETR
import cv2
import os
import numpy as np
from tqdm import tqdm

# Load the YOLOv8 model
model = RTDETR(r'E:\detr\Code3\runs\detect\rtdetr_experiment94\weights\best.pt')

# Function to calculate IoU (Intersection over Union)
def compute_iou(box1, box2):
    x1, y1, x2, y2 = box1
    x1_b, y1_b, x2_b, y2_b = box2

    # Calculate the intersection
    inter_x1 = max(x1, x1_b)
    inter_y1 = max(y1, y1_b)
    inter_x2 = min(x2, x2_b)
    inter_y2 = min(y2, y2_b)
    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

    # Calculate the union
    box1_area = (x2 - x1) * (y2 - y1)
    box2_area = (x2_b - x1_b) * (y2_b - y1_b)
    union_area = box1_area + box2_area - inter_area

    if union_area == 0:
        return 0
    return inter_area / union_area

# Function to remove duplicate boxes based on IoU
def remove_duplicates(boxes, scores, iou_threshold=0.5):
    keep = []
    indices = np.argsort(scores)[::-1]  # Sort by confidence score in descending order

    while len(indices) > 0:
        current = indices[0]
        keep.append(current)

        # Compute IoU between the current box and the rest
        iou = np.array([compute_iou(boxes[current], boxes[i]) for i in indices[1:]])

        # Keep boxes with IoU less than the threshold
        indices = indices[1:][iou < iou_threshold]

    return keep

# Run model inference
results = model(
    source=r'E:\detr\private_test\private test',
    conf=0.2,
    augment=False,
    device='0',
    nms=True
)

# Write results to `predict.txt`
output_file = 'predict.txt'
with open(output_file, 'w') as f:
    for result in tqdm(results):
        image_name = os.path.basename(result.path)  # Extract image file name
        img_width, img_height = result.orig_shape[1], result.orig_shape[0]  # Image dimensions

        # Extract boxes, scores, and classes
        boxes = np.array([box.xyxy[0].cpu().numpy() for box in result.boxes])
        scores = np.array([box.conf[0].cpu().numpy() for box in result.boxes])
        classes = np.array([int(box.cls[0]) for box in result.boxes])

        # Remove duplicates using NMS
        keep_indices = remove_duplicates(boxes, scores)

        # Process each remaining detection
        for i in keep_indices:
            x1, y1, x2, y2 = boxes[i]
            confidence = scores[i]
            class_id = classes[i]

            # Normalize and calculate bounding box details
            x_center = ((x1 + x2) / 2) / img_width
            y_center = ((y1 + y2) / 2) / img_height
            width = (x2 - x1) / img_width
            height = (y2 - y1) / img_height

            # Write to file
            f.write(f'{image_name} {class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f} {confidence:.2f}\n')

print(f"Predictions saved to {output_file}")

# Define colors for different labels
label_colors = {
    0: (0, 255, 0),  # Green
    1: (0, 255, 255),  # Yellow
    2: (255, 0, 0),  # Blue
    3: (0, 0, 255),  # Red
}

# Helper function to find the next available output directory
def get_next_predict_dir(base_path, prefix="predict"):
    i = 1
    while True:
        dir_name = f"{prefix}{i}"
        dir_path = os.path.join(base_path, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            return dir_path
        i += 1

# Get output directory
base_path = r'E:/detr/Result2/runs/detect'
output_dir = get_next_predict_dir(base_path)
print(f"Saving annotated images to: {output_dir}")

# Process and annotate each result image
for result in tqdm(results):
    image_path = result.path
    img = cv2.imread(image_path)

    if img is None:
        print(f"Warning: Unable to read image at {image_path}")
        continue

    # Extract boxes, scores, and classes
    boxes = np.array([box.xyxy[0].cpu().numpy() for box in result.boxes])
    scores = np.array([box.conf[0].cpu().numpy() for box in result.boxes])
    classes = np.array([int(box.cls[0]) for box in result.boxes])

    # Remove duplicates using NMS
    keep_indices = remove_duplicates(boxes, scores)

    for i in keep_indices:
        x1, y1, x2, y2 = map(int, boxes[i])
        conf = scores[i]
        class_id = classes[i]

        color = label_colors.get(class_id, (0, 255, 0))

        cv2.rectangle(img, (x1, y1), (x2, y2), color, 1)
        cv2.putText(img, f'{conf:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    output_image_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(output_image_path, img)

print("Annotation complete.")
