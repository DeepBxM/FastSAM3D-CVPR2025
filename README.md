# fastsam3D


# Medical Image Preprocessing Pipeline

本项目用于对医学图像进行预处理，包括标签提取、文件格式转换、结构化组织以及评估结果的保存。以下为项目的各个步骤说明。

---


##  Getting Started

**System Requirements:**

* **Python**: `version 3.9 or above`
* **CUDA**: `version 12.1`
* **FLASH Attention support GPU**: `Ampere, Ada, or Hopper GPUs (e.g., A100, RTX 3090, RTX 4090, H100).`


###  Installation

<h4>From <code>source</code></h4>

> 1. Clone the FastSAM3D-v1 repository:
>
> ```console
> $ git clone https://github.com/skill-diver/FastSAM3D-v1
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd FastSAM3D-v1
> ```
>
> 3. Install the dependencies:
> ```console
> $ pip install -r requirements.txt


###  Usage

<h4>From <code>source</code></h4>

> 1.Prepare Your Training Data (from nnU-Net-style dataset): 

> Ensure that your training data is organized according to the structure shown in the `data/medical_preprocessed` directories. The target file structures should be like the following:
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



## 📁 数据结构说明

初始目录包含以下文件：

- `gts_npz/`：包含 `.npz` 格式的标签数据（标签保存在 `label.npy`）
- `labels/`：空或初始目录，用于保存中间生成的 `label.nii.gz`
- `image.npz`：包含原始图像数据（保存为 `imgs.npy`）
- `structure.json`：包含图像结构的 JSON 映射信息

---

## 🔧 步骤说明

### 1️⃣ 将所有 `gts_npz` 中的标签 `.npz` 转换为 `label.nii.gz`

从每个 `.npz` 文件中提取 `gts.npy`，并保存为 `label.nii.gz` 格式，写入到 `labels/` 文件夹中。

---

### 2️⃣ 根据 `structure.json` 的顶层键，将对应的 `label.nii.gz` 分类

- 读取 `CVPR25.json` 顶层键
- 遍历 `labels/` 中的 `label.nii.gz`
  - 如果键名匹配：
    - 在指定文件夹中以键名创建子文件夹
    - 将对应的 `label.nii.gz` 移动到该子文件夹中
  - 如果键名不匹配：
    - 不做处理，保留在 `labels/` 中

---

### 3️⃣ 对剩余未匹配的 `label.nii.gz`，更新 JSON 文件

使用特定规则（如使用图像内容、文件名、路径信息等）为这些文件提取新的键名，并更新到 `CVPR25.json` 中。


---

### 4️⃣ 按照 JSON 文件中的标签定义，对每个标签进行提取并分类存储

- 对 `label.nii.gz` 中的每个标签进行分割提取
- 根据标签名创建对应子文件夹
- 将提取的标签图像保存至对应子文件夹下

---

### 5️⃣ 将 `image.npz` 中的 `imgs.npy` 转换为 `image.nii.gz`

- 读取 `imgs.npy` 并保存为 `image.nii.gz` 格式

---

### 6️⃣ 移动 `image.nii.gz` 到每个器官子文件夹的 `imagesTr/` 中

- 每个器官子文件夹内新建 `imagesTr/`
- 将对应的 `image.nii.gz` 移动进去

---

### 7️⃣ 重命名图像和标签文件，去除后缀 `_image` 和 `_label`

例如：


---

### 8️⃣ 保存模型预测结果 `pred4`

将模型预测的第 4 个版本结果（`pred4`）保存为指定格式，结构与原始标签一致。

---

### 9️⃣ 验证集结果转换为 `.npz` 格式并保存

- 将验证集的预测结果（如 `.nii.gz`）转换为 `.npz` 格式
- 每个 `.npz` 包含两个键：
  - `labels.npy`
  - `spacing.npy`
- 所有 `.npz` 保存在一个统一的输出文件夹中

---🔟

## 📌 项目目标

实现标准化的医学图像预处理流程，便于后续模型训练与评估，支持用于 MICCAI、SegTHOR、AMOS 等医学图像任务的数据集结构。

---

## 📞 联系方式

如需更多帮助或协作，请联系项目负责人。

---

