# FastSAM3D (CVPR 2025)

FastSAM3D is an efficient 3D medical image segmentation framework, leveraging the power of Segment Anything and SAM-Med3D. This project aims for rapid 3D segmentation of general organs and is applicable to a variety of medical imaging tasks.

---

##  System Requirements

- **Python** ≥ 3.9  
- **CUDA** = 12.1  
- **GPU Requirements**: GPUs supporting FLASH Attention, such as A100, RTX 3090/4090, H100 (Ampere, Ada, Hopper architectures)

---

##  Installation

### Install from Source

```bash
# Clone the repository
git clone https://github.com/skill-diver/FastSAM3D-v1
cd FastSAM3D-v1

# Install dependencies
pip install -r requirements.txt
```
---

> ```
> data/medical_preprocessed
>       ├── adrenal
>       │ ├── ct_WORD
>       │ │ ├── imagesTr
>       │ │ │ ├── word_0025.nii.gz
>       │ │ │ ├── ...
>       │ │ ├── labelsTr
>       │ │ │ ├── word_0025.nii.gz
>       │ │ │ ├── ...
>       ├── ...
> ```

---

## steps

### 1 Prepare Your Training Data

Organize all NPZ files containing gts.npy from the validation set into the 'labels' folder. The  `classify.py` script can convert NPZ files to NII.GZ format and categorize them based on  `CVPR25.json`.

>    ```console
>    python classify.py
>    ```

Categorize all .nii.gz files into subfolders based on the top-level keys in the corresponding JSON files, creating the subfolders as needed.

>    ```console
>    python categorize.py
>    ```

Convert the imgs.npy array from image.npz to NIfTI format image.nii.gz, then move it to respective organ-specific subfolders' imagesTr/ directories and standardize filenames by removing _image/_label suffixes.

>    ```console
>    python reallocate.py
>    ```

---

### 2 Modify `utils/data_paths.py` based on your own data. 
> ```
> img_datas = [
> "data/train/adrenal/ct_WORD",
> "data/train/liver/ct_WORD",
> ...
> ]
> ```

---

### 3 Train the Teacher Model and Prepare Labels(logits)

To train the teacher model and prepare labels for guided distillation to the student model, run the command below. Ensure your data and checkpoint are placed in the designated locations within the shell script.

>    ```console
>    python preparelabel.py
>    ```

---

### 4 Distill the Model

To perform distillation, run the command below. The distilled checkpoint will be saved in  `work_dir`. Ensure your data and checkpoint paths are correctly specified in the shell script.

>    ```console
>    python distillation.py
>    ```

---

### 5 Validate the Teacher Model

To validate the teacher model, run the command below. Ensure your data and the teacher model checkpoint (linked below) are correctly placed in the shell script.

>    ```console
>    python validation.py
>    ```

---

### 6 Validate FastSAM3D model, or your distilled student model

To validate the distilled student model, run the command below. Ensure your data, teacher model, and FastSAM3D checkpoint (linked below) are properly placed in the shell script.

>    ```console
>    python validation_student.py
>    ```

---

### 7 change to `.npz` 

Save the model prediction result `pred4`.(if num_clicks=5) 
Convert the validation set prediction results (e.g., `.nii.gz`) into `.npz` format, where each file contains `labels.npy` and `spacing.npy`, and save them in a unified output folder.

>    ```console
>    python convert_npz.py
>    ```

---

## Checkpoints

Below are the links to the checkpoints for FastSAM3D and its fine-tuned version:

| Model                | Download Link |
|----------------------|---------------|
| FASTSAM3D            | [Download](https://huggingface.co/techlove/FastSAM3D/tree/main) |
| Teacher Model        | [Download](https://huggingface.co/blueyo0/SAM-Med3D/blob/main/sam_med3d_turbo.pth) |


---
