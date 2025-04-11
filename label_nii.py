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


def convert_folder_npz_to_nifti(input_dir, output_dir):
    """
    遍历文件夹，转换所有 .npz 文件中的 gts.npy 为 .nii.gz

    参数:
    - input_dir: 存放 .npz 文件的目录
    - output_dir: 存放转换后 .nii.gz 文件的目录
    """
    os.makedirs(output_dir, exist_ok=True)  # 确保输出目录存在

    for filename in os.listdir(input_dir):
        if filename.endswith('.npz'):
            npz_path = os.path.join(input_dir, filename)
            print(f"正在处理: {npz_path}")

            data = np.load(npz_path)
            if 'gts' not in data:
                print(f"警告: {filename} 中没有 'gts'，跳过...")
                continue

            gts = data['gts']

            # 获取文件名主体部分（去掉扩展名）
            base_name = os.path.splitext(filename)[0]  # 去掉 `.npz`
            output_filename = f"{base_name}_label.nii.gz"
            output_path = os.path.join(output_dir, output_filename)

            # 保存 gts 到 .nii.gz
            save_to_nifti(gts, output_path, is_label=True)

    print("所有文件转换完成！")


# 设定输入和输出路径
input_directory = ''
output_directory = ''

# 运行转换
convert_folder_npz_to_nifti(input_directory, output_directory)
