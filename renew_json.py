import os
import json
import re
import numpy as np
import nibabel as nib


def extract_top_key(filename):
    """
    从 nii.gz 文件名中提取顶层键。
    保留从左向右检测的第三个 "_" 之前的内容作为顶层键名。
    """
    # 去除尾部扩展名
    if filename.endswith('_label.nii.gz'):
        base = filename[:-len('_label.nii.gz')]
    elif filename.endswith('.nii.gz'):
        base = filename[:-len('.nii.gz')]
    else:
        base = filename

    # 找到第三个 "_" 的位置
    underscore_indices = [i for i, char in enumerate(base) if char == '_']
    if len(underscore_indices) >= 3:
        # 保留第三个 "_" 之前的内容
        top_key = base[:underscore_indices[2]]
    else:
        # 如果不足三个 "_"，则返回整个字符串
        top_key = base

    return top_key


def get_unique_labels(nii_path):
    """
    加载 nii.gz 文件并返回图像中唯一标签值（使用 numpy.unique）
    """
    try:
        img = nib.load(nii_path)
        data = img.get_fdata()
        # 对于标签值通常为整数，可以先转换为整数再求唯一值
        unique_vals = np.unique(data.astype(np.int32))
        return unique_vals.tolist()
    except Exception as e:
        print(f"读取文件 {nii_path} 出错: {e}")
        return []


def generate_json_entry(top_key, unique_labels, instance_label):
    """
    根据顶层键和唯一标签生成一个 JSON 条目，
    格式类似原始 JSON 模板，其中每个标签对应一个描述列表。
    """
    entry = {}
    # 遍历除背景标签（假设 0 为背景，可根据需要调整）
    for label in unique_labels:
        # 如果不希望生成背景的描述，可以跳过 label==0
        if label == 0:
            continue
        label_str = str(label)
        # 生成描述列表（这里只给出三个默认描述）
        descriptions = [
            f"{top_key} label {label_str} description 1",
            f"{top_key} label {label_str} description 2",
            f"{top_key} label {label_str} description 3"
        ]
        entry[label_str] = descriptions
    entry["instance_label"] = instance_label
    return entry


def update_json_with_leftover(json_path, labels_dir, output_json_path):
    """
    对于仍保留在 labels 目录中的 nii.gz 文件：
      1. 检查每个文件的标签值
      2. 根据文件名提取顶层键（自动分组）
      3. 根据原有 JSON 模板自动生成新条目，并合并更新到原 JSON 中
    最后保存为 output_json_path
    """
    # 加载原始 JSON，如果不存在则新建空字典
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            orig_json = json.load(f)
    else:
        orig_json = {}

    # 获取当前已有的 instance_label 最大值（假设为整数）
    existing_labels = [v.get("instance_label", -1) for v in orig_json.values() if isinstance(v, dict)]
    next_instance_label = max(existing_labels) + 1 if existing_labels else 0

    # 获取 labels 目录中的所有 nii.gz 文件
    nii_files = [f for f in os.listdir(labels_dir) if f.endswith('.nii.gz')]
    print(f"在 labels 目录中找到 {len(nii_files)} 个 nii.gz 文件待处理。")

    # 按提取的顶层键分组文件
    groups = {}
    for nii_file in nii_files:
        top_key = extract_top_key(nii_file)
        groups.setdefault(top_key, []).append(nii_file)

    print("根据文件名提取到的顶层键如下：")
    for key, files in groups.items():
        print(f"  {key}: {len(files)} 个文件")

    # 对于每个分组，读取其中一个文件以获得标签值，然后生成 JSON 条目（如果该键不在原 JSON 中）
    for top_key, files in groups.items():
        if top_key in orig_json:
            print(f"跳过已存在的键：{top_key}")
            continue

        # 使用组内第一个文件来获取标签值
        sample_file = os.path.join(labels_dir, files[0])
        unique_labels = get_unique_labels(sample_file)
        print(f"文件组 {top_key} 的唯一标签: {unique_labels}")

        # 生成 JSON 条目
        entry = generate_json_entry(top_key, unique_labels, next_instance_label)
        orig_json[top_key] = entry
        print(f"为键 {top_key} 分配 instance_label = {next_instance_label}")
        next_instance_label += 1  # 更新 instance_label

    # 保存更新后的 JSON
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(orig_json, f, indent=4, ensure_ascii=False)
    print(f"更新后的 JSON 已保存到 {output_json_path}")


# 使用示例，请根据实际路径修改
# 原始 JSON 模板文件路径
json_path = "./CVPR25 (copy).json"
# labels 目录中仍保留的 nii.gz 文件所在的目录
labels_dir = "/media/wagnchogn/ssd_2t/lmy/step/val_no_json (copy)/labels"
# 输出更新后的 JSON 文件路径
output_json_path = "./val_new/updated_data.json"

update_json_with_leftover(json_path, labels_dir, output_json_path)
