	import os
import json
import shutil


def organize_nii_files(json_path, labels_dir, output_dir):
    # 确保 JSON 文件存在
    if not os.path.exists(json_path):
        print(f"❌ 错误：JSON 文件 {json_path} 不存在！")
        return

    # 读取 JSON 文件
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 获取所有顶层键
    top_keys = set(data.keys())
    print(f"✅ JSON 文件中的顶层键：{top_keys}")

    # 确保 labels 文件夹存在
    if not os.path.exists(labels_dir):
        print(f"❌ 错误：labels 文件夹 {labels_dir} 不存在！")
        return

    # 获取 labels 目录中的所有 .nii.gz 文件
    nii_files = [f for f in os.listdir(labels_dir) if f.endswith('.nii.gz')]
    print(f"✅ 找到 {len(nii_files)} 个 nii.gz 文件：{nii_files}")

    moved_files = 0  # 计数已移动的文件
    unmatched_files = []  # 记录未匹配的文件

    # 遍历 nii.gz 文件并进行模糊匹配
    for nii_file in nii_files:
        matched = False
        for key in top_keys:
            if key in nii_file:  # 只要文件名中包含键名，就算匹配
                # 目标子文件夹
                target_folder = os.path.join(output_dir, key)
                os.makedirs(target_folder, exist_ok=True)

                # 移动文件
                src_path = os.path.join(labels_dir, nii_file)
                dst_path = os.path.join(target_folder, nii_file)

                if os.path.exists(src_path):
                    shutil.move(src_path, dst_path)
                    moved_files += 1
                    print(f"✅ 移动 {nii_file} -> {target_folder}")
                else:
                    print(f"⚠️ 警告：文件 {nii_file} 在 labels 目录中不存在！")

                matched = True  # 记录匹配成功
                break  # 一个文件最多匹配一个键，避免重复匹配

        if not matched:
            unmatched_files.append(nii_file)  # 记录未匹配的文件

    print(f"\n�� 任务完成，共移动 {moved_files} 个文件。")
    print(f"�� 仍然保留在 labels 目录中的 {len(unmatched_files)} 个文件：{unmatched_files}")


# 使用示例（请修改路径）
json_path = "./CVPR25 (copy).json"  # JSON 文件路径
labels_dir = "/media/wagnchogn/ssd_2t/lmy/step/val_new (copy)/labels"  # labels 文件夹路径
output_dir = "./validation"  # 目标存放文件的路径

organize_nii_files(json_path, labels_dir, output_dir)
