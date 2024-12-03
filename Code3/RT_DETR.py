from ultralytics import RTDETR
# from ultralytics import YOLO
# Ensure RTDETR is available in ultralytics
import os
import torch

# Paths
MODEL_PATH = 'rtdetr-x.pt'  # Path to pre-trained weights
DATASET_PATH = r"E:\detr\Full_data_Augmentation\coco8\coco8.yaml"  # Dataset config YAML

if __name__ == '__main__':
    # Ensure pre-trained model exists
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at: {MODEL_PATH}")
    torch.cuda.empty_cache()
    # Optionally disable deterministic algorithms for speed (only if necessary)
    torch.use_deterministic_algorithms(False)

    # Load pre-trained RT-DETR model (Ensure the correct method is used for loading weights)
    model = RTDETR(MODEL_PATH)

    # Train the model
    model.train(
        data=DATASET_PATH,
        epochs=50,
        imgsz=640,
        batch=16,
        iou=0.4,
        device="0",  # Use GPU 0
        name='rtdetr_experiment',
        # augment=False,
        cache=False,  # Disable cache
        amp=True,  # Enable mixed precision
        patience=20,  # Early stopping
        nms = True,
        # data_loader=torch.utils.data.DataLoader(),
    )

    # Evaluate on the validation set
    validation_metrics = model.val()  # Store validation metrics separately
    print(f"Validation Metrics: {validation_metrics}")

    # Evaluate on the test set
    test_metrics = model.test()  # Store test metrics separately
    print(f"Test Metrics: {test_metrics}")

    # Optionally, save the model after training (for future use)
    model.save('rtdetr_trained_model.pt')  # Save final trained model to disk
