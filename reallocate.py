import os
import shutil

def move_images_to_imagestr(images_dir, val_new_dir):
    # 收集所有图像文件的名称和路径（仅处理包含'_image'的文件）
    image_files = {}
    for filename in os.listdir(images_dir):
        if filename.endswith('.nii.gz') and '_image' in filename:
            image_files[filename] = os.path.join(images_dir, filename)

    # 遍历val_new目录下的所有labelsTr文件夹
    for root, dirs, files in os.walk(val_new_dir):
        if os.path.basename(root) == 'labelsTr':
            for label_file in files:
                if label_file.endswith('_label.nii.gz'):
                    # 构造对应的图像文件名
                    image_filename = label_file.replace('_label', '_image')
                    if image_filename in image_files:
                        src_path = image_files[image_filename]
                        # 获取对应的CT目录路径（labelsTr的父目录）
                        ct_dir = os.path.dirname(root)
                        # 创建imagesTr目录
                        images_tr_dir = os.path.join(ct_dir, 'imagesTr')
                        os.makedirs(images_tr_dir, exist_ok=True)
                        # 移动图像文件
                        dest_path = os.path.join(images_tr_dir, image_filename)
                        shutil.move(src_path, dest_path)
                        print(f"Moved: {src_path} -> {dest_path}")
                        # 从字典中移除已处理的文件（避免重复处理）
                        del image_files[image_filename]
                    else:
                        print(f"Image not found: {image_filename} (Label: {label_file})")

    # 检查是否还有未处理的图像文件
    if image_files:
        print("\n以下图像文件未找到对应的标签文件:")
        for remaining in image_files:
            print(remaining)

# 配置路径并执行函数
if __name__ == "__main__":
    images_dir = './images'       # 原始图像目录路径
    val_new_dir = './val_with_organ'      # 目标结构根目录路径
    move_images_to_imagestr(images_dir, val_new_dir)
