import numpy as np
import nibabel as nib
import os


def save_to_nifti(data, save_path, is_label=False):
    """
    将 numpy 数组保存为 .nii.gz 格式

    参数:
    - data: numpy 数组，图像或标签数据
    - save_path: 保存路径
    - is_label: 是否为标签数据（影响数据类型）
    """
    if is_label:
        data = data.astype(np.uint8)  # 标签数据转换为 uint8
    else:
        data = data.astype(np.float32) if data.dtype == np.float64 else data

    affine = np.eye(4)  # 单位仿射矩阵
    nifti_img = nib.Nifti1Image(data, affine)

    if is_label:
        nifti_img.header.set_data_dtype(np.uint8)

    nib.save(nifti_img, save_path)
    print(f"已保存: {save_path}")


def convert_folder_npz_to_nifti(input_dir):
    """
    遍历文件夹，转换所有 .npz 文件中的 imgs.npy 为 .nii.gz，并删除原始 .npz 文件

    参数:
    - input_dir: 存放 .npz 文件的目录
    """
    for filename in os.listdir(input_dir):
        if filename.endswith('.npz'):
            npz_path = os.path.join(input_dir, filename)
            print(f"正在处理: {npz_path}")

            data = np.load(npz_path)
            if 'imgs' not in data:
                print(f"警告: {filename} 中没有 'imgs'，跳过...")
                continue

            imgs = data['imgs']

            # 获取文件名主体部分（去掉扩展名）
            base_name = os.path.splitext(filename)[0]  # 去掉 `.npz`
            output_filename = f"{base_name}_image.nii.gz"  # 按照指定格式命名
            output_path = os.path.join(input_dir, output_filename)

            # 保存 imgs 到 .nii.gz
            save_to_nifti(imgs, output_path, is_label=False)

            # 删除原始 .npz 文件
            os.remove(npz_path)
            print(f"已删除: {npz_path}")

    print("所有文件转换完成！")


# 设定输入路径
input_directory = './images'

# 运行转换
convert_folder_npz_to_nifti(input_directory)
