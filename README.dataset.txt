# bib number labeling > 2023-12-16 8:33am
https://universe.roboflow.com/marco-cheung/bib-number-labeling

Provided by a Roboflow user
License: CC BY 4.0

A computer vision model for racing bib number (RBN) detection.

**Training data:**
This model was trained on custom datasets consisting of my self-annotated images and multiple public datasets related to bib-number class available on Roboflow Universe, including:

https://universe.roboflow.com/thomas-lamalle/bib-detection
https://universe.roboflow.com/rbnr/bib-detector
https://universe.roboflow.com/sputtipa/bip
https://universe.roboflow.com/bibnumber/bibnumber
https://universe.roboflow.com/python-vertiefung/python-vertiefung
https://universe.roboflow.com/hcmus-3p8wh/bib-detection-big-data
https://universe.roboflow.com/h1-qtgu0/bib-number

To improve the ability of model prediction power on unseen images, image augmentation techniques are applied to existing 2687 images from the above combined datasets. As a result, a total of 6655 images were used to train this RBN detection model using ***YOLOv8l*** as base model.

**Compute Infrastructure:**
The model was trained and fine-tuned in Jupyter Lab environment on GCP Vertex AI Platform, with support of a NVIDIA A100 GPU to accelerate training process.
