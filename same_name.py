import os
import re
import shutil


def rename_nii_files(root_dir):
    """
    递归遍历目录，将文件名中的'_image'或'_label'后缀删除
    格式要求：xxx_image.nii.gz → xxx.nii.gz
    """
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith(".nii.gz"):
                # 使用正则表达式匹配并删除末尾的_image或_label
                new_name = re.sub(
                    r"(_image|_label)(\.nii\.gz)$",
                    r"\2",  # 保留.nii.gz部分
                    filename
                )

                # 如果新文件名与旧文件名不同，则重命名
                if new_name != filename:
                    old_path = os.path.join(root, filename)
                    new_path = os.path.join(root, new_name)

                    # 避免覆盖已有文件
                    if not os.path.exists(new_path):
                        shutil.move(old_path, new_path)
                        print(f"Renamed: {filename} → {new_name}")
                    else:
                        print(f"⚠️ 冲突: {new_name} 已存在，跳过 {filename}")


if __name__ == "__main__":
    target_dir = "/media/wagnchogn/ssd_2t/lmy/FastSAM3D_copy/data_10per/val_with_organ (copy)"  # 修改为你的根目录
    rename_nii_files(target_dir)
