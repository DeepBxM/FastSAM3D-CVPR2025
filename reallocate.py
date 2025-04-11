import numpy as np
import nibabel as nib
import os
import shutil

def save_to_nifti(data, save_path, is_label=False):
    """
    Save numpy array as .nii.gz format

    Args:
    - data: numpy array, image or label data
    - save_path: path to save the .nii.gz file
    - is_label: whether the data is label (affects dtype)
    """
    if is_label:
        data = data.astype(np.uint8)
    else:
        data = data.astype(np.float32) if data.dtype == np.float64 else data

    affine = np.eye(4)  # identity affine matrix
    nifti_img = nib.Nifti1Image(data, affine)

    if is_label:
        nifti_img.header.set_data_dtype(np.uint8)

    nib.save(nifti_img, save_path)
    print(f"Saved: {save_path}")

def convert_folder_npz_to_nifti(input_dir):
    """
    Convert all .npz files in a folder (with key 'imgs') to .nii.gz format
    and delete the original .npz files.

    Args:
    - input_dir: directory containing .npz files
    """
    for filename in os.listdir(input_dir):
        if filename.endswith('.npz'):
            npz_path = os.path.join(input_dir, filename)
            print(f"Processing: {npz_path}")

            data = np.load(npz_path)
            if 'imgs' not in data:
                print(f"Warning: 'imgs' not found in {filename}, skipping...")
                continue

            imgs = data['imgs']
            base_name = os.path.splitext(filename)[0]
            output_filename = f"{base_name}_image.nii.gz"
            output_path = os.path.join(input_dir, output_filename)

            save_to_nifti(imgs, output_path, is_label=False)
            os.remove(npz_path)
            print(f"Deleted: {npz_path}")

    print("All .npz files have been converted to .nii.gz!")

def move_images_to_imagestr(images_dir, val_new_dir):
    """
    Move converted image files to corresponding imagesTr folders
    based on label file structure.

    Args:
    - images_dir: directory containing image .nii.gz files
    - val_new_dir: root directory containing label folders
    """
    image_files = {}
    for filename in os.listdir(images_dir):
        if filename.endswith('.nii.gz') and '_image' in filename:
            image_files[filename] = os.path.join(images_dir, filename)

    for root, dirs, files in os.walk(val_new_dir):
        if os.path.basename(root) == 'labelsTr':
            for label_file in files:
                if label_file.endswith('_label.nii.gz'):
                    image_filename = label_file.replace('_label', '_image')
                    if image_filename in image_files:
                        src_path = image_files[image_filename]
                        ct_dir = os.path.dirname(root)
                        images_tr_dir = os.path.join(ct_dir, 'imagesTr')
                        os.makedirs(images_tr_dir, exist_ok=True)
                        dest_path = os.path.join(images_tr_dir, image_filename)
                        shutil.move(src_path, dest_path)
                        print(f"Moved: {src_path} -> {dest_path}")
                        del image_files[image_filename]
                    else:
                        print(f"Image not found for label: {label_file}")

    if image_files:
        print("\nThe following image files do not have corresponding label files:")
        for remaining in image_files:
            print(remaining)

if __name__ == "__main__":
    images_dir = './images'            # path to .npz files and temporary output .nii.gz
    val_new_dir = './val'   # root directory containing labelsTr folders

    # Step 1: Convert .npz files to .nii.gz
    convert_folder_npz_to_nifti(images_dir)

    # Step 2: Move .nii.gz image files into appropriate imagesTr folders
    move_images_to_imagestr(images_dir, val_new_dir)
