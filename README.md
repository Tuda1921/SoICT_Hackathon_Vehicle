# Instructions for Training and Running the Model
Data Augmentation Check:
Check the Full_data_Augmentation folder for data augmentation.

Path Updates:
Update the path to the COCO folder in coco8.yaml inside the datasets-full folder.
Update the path to the COCO folder in coco8.yaml inside the Full_data_Augmentation folder.

Model Training:
Open the Code3 folder.
Modify the DATASET_PATH in the RT_DETR.py file.
Run the RT_DETR.py file in the Code3 folder to start training the model.

Running Results:
Open the Run_Result_RT_DETR.py file in the Result2 folder.
Adjust the path to the best weight file located in Code3\runs\detect\rtdetr_experiment35\weights (this will be available after training).
The results will be saved in the Result2 folder.

Important Parameters to Note:
Pay attention to the IoU during both training and inference.
Key fine-tuning parameters include:iou, nms, agnostic nms, conf, lr, batch_size
