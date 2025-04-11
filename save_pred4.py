import os
import re

def delete_non_pred4_files(root_dir):
    """
    递归删除所有以_predX.nii.gz结尾（X≠4）的文件
    保留格式：xxx_pred4.nii.gz
    """
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith(".nii.gz"):
                # 检测是否符合_predX.nii.gz格式
                if re.search(r'_pred\d+\.nii\.gz$', filename):
                    # 仅删除非_pred4文件
                    if not filename.endswith("_pred4.nii.gz"):
                        file_path = os.path.join(root, filename)
                        os.remove(file_path)
                        print(f"已删除: {file_path}")
                    else:
                        print(f"保留: {os.path.join(root, filename)}")

if __name__ == "__main__":
    target_dir = "./val_stu_5"  # 修改为你的根目录
    delete_non_pred4_files(target_dir)
