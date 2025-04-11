import os
import json
import shutil
import numpy as np
import nibabel as nib


def load_json(json_path):
    """ 加载JSON文件 """
    with open(json_path, 'r') as f:
        return json.load(f)


def extract_labels_from_nii(nii_path):
    """ 读取 nii.gz 文件，提取唯一的标签值（去除背景0） """
    img = nib.load(nii_path)
    data = img.get_fdata()
    unique_labels = np.unique(data).astype(int)  # 获取唯一标签值
    unique_labels = unique_labels[unique_labels > 0]  # 去掉背景 0
    return unique_labels


def get_organ_name(label, json_data, dataset_name):
    """ 从JSON中获取标签对应的器官名称 """
    dataset_info = json_data.get(dataset_name, {})
    return dataset_info.get(str(label), [None])[0]  # 取第一个器官名称


def organize_dataset(dataset_folder, json_path, output_folder):
    """
    读取 dataset_folder 中的所有子目录，提取 label.nii.gz 文件的标签，并重组数据结构
    dataset_folder: 原始数据集的根目录（包含 CT_AbdomenAtlas, CT_AMOS, MR_AMOS 等）
    json_path: JSON 文件路径
    output_folder: 目标输出路径
    """
    json_data = load_json(json_path)

    # 遍历 dataset_folder 中的所有子文件夹（如 CT_AbdomenAtlas, CT_AMOS, MR_AMOS）
    for dataset_name in os.listdir(dataset_folder):
        dataset_path = os.path.join(dataset_folder, dataset_name)
        if not os.path.isdir(dataset_path):
            continue

        # 遍历子文件夹中的 nii.gz 文件
        for file_name in os.listdir(dataset_path):
            if not file_name.endswith('.nii.gz'):
                continue

            nii_path = os.path.join(dataset_path, file_name)
            unique_labels = extract_labels_from_nii(nii_path)

            for label in unique_labels:
                organ_name = get_organ_name(label, json_data, dataset_name)
                if organ_name is None:
                    continue

                organ_name = organ_name.replace(" ", "_")  # 替换空格
                organ_folder = os.path.join(output_folder, "val_1", organ_name, dataset_name, "labelsTr")

                # 创建目录并复制文件
                os.makedirs(organ_folder, exist_ok=True)
                shutil.copy(nii_path, os.path.join(organ_folder, file_name))
                print(f"已移动 {file_name} 到 {organ_folder}")


# 运行代码
dataset_folder = "./validation"  # 你的数据集文件夹，包含 CT_AbdomenAtlas, CT_AMOS, MR_AMOS
json_path = "./CVPR25.json"  # JSON 文件路径
output_folder = "./val_new"  # 目标输出文件夹

organize_dataset(dataset_folder, json_path, output_folder)
