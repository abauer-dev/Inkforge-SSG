
import os
import shutil


def copy_files_recursive(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        raise ValueError(f"Source directory does not exist: {source_dir}")

    # Wipe the destination so the copy is clean.
    # On recursive calls into subdirectories, dest_dir doesn't exist yet
    # (its parent was just created above it), so rmtree is skipped and
    # we just mkdir the new subdir. The deletion is only meaningful on
    # the top-level call.
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)

    for item in os.listdir(source_dir):
        source_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(source_path):
            print(f"  copy file: {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            print(f"  enter dir: {source_path} -> {dest_path}")
            copy_files_recursive(source_path, dest_path)


def main():
    copy_files_recursive("/home/linuxab/workspace/ab/static-site/static", "/home/linuxab/workspace/ab/static-site/public")

main()