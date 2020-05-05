import os
import shutil
import random
import glob
import cv2
import argparse
dir_path = '/Users/sunbowen/Desktop/images/project/tuatua/resized_tua'
# des_path = '/Users/sunbowen/Desktop/images/project/mussel/resized_mus'


# Rename files from .jpeg to .jpg
def rename():
    files = os.listdir(dir_path)

    for file in files:
        pre, ext = os.path.splitext(file)
        os.rename(dir_path + '/' + file, dir_path + '/t_' + pre + '.jpg')


# allocate data to train and test
def allocate_data():
    files = random.sample(os.listdir(dir_path), 22)

    for file in files:
        srcpath = os.path.join(dir_path, file)
        print(srcpath)
        shutil.move(srcpath, destination, copy_function=shutil.copytree)


def resize_img():
    parser = argparse.ArgumentParser(
        description="Resize raw images to uniformed target size."
    )
    parser.add_argument(
        "--raw-dir",
        help="Directory path to raw images.",
        default="/Users/sunbowen/Desktop/images/project/cockle/raw_cockle",
        type=str,
    )
    parser.add_argument(
        "--save-dir",
        help="Directory path to save resized images.",
        default="/Users/sunbowen/Desktop/images/project/cockle/resized_cockle",
        type=str,
    )
    parser.add_argument(
        "--ext", help="Raw image files extension to resize.", default="jpg", type=str
    )
    parser.add_argument(
        "--target-size",
        help="Target size to resize as a tuple of 2 integers.",
        default="(800, 600)",
        type=str,
    )
    args = parser.parse_args()

    raw_dir = args.raw_dir
    save_dir = args.save_dir
    ext = args.ext
    target_size = eval(args.target_size)
    msg = "--target-size must be a tuple of 2 integers"
    assert isinstance(target_size, tuple) and len(target_size) == 2, msg
    fnames = glob.glob(os.path.join(raw_dir, "*.{}".format(ext)))
    os.makedirs(save_dir, exist_ok=True)
    print(
        "{} files to resize from directory `{}` to target size:{}".format(
            len(fnames), raw_dir, target_size
        )
    )
    for i, fname in enumerate(fnames):
        print(".", end="", flush=True)
        img = cv2.imread(fname)
        img_small = cv2.resize(img, target_size)
        new_fname = "{}.{}".format(str(i), ext)
        small_fname = os.path.join(save_dir, new_fname)
        cv2.imwrite(small_fname, img_small)
    print(
        "\nDone resizing {} files.\nSaved to directory: `{}`".format(
            len(fnames), save_dir
        )
    )


if __name__ == "__main__":
    # allocate_data()
    rename()
    # resize_img()
