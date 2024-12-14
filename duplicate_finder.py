import os
from PIL import Image
import imagehash

def find_duplicate_images(directory):
    """
    Find duplicate images in a directory based on perceptual hashing.

    :param directory: Path to the directory containing images.
    :return: A dictionary where keys are hash values and values are lists of file paths.
    """
    hash_dict = {}
    duplicates = {}

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            print("checking...", file_path)
            try:
                with Image.open(file_path) as img:
                    # Generate perceptual hash
                    img_hash = imagehash.phash(img)

                # Check for duplicates
                if img_hash in hash_dict:
                    duplicates.setdefault(img_hash, []).append(file_path)
                else:
                    hash_dict[img_hash] = file_path
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    return duplicates

def main():
    directory = r"\\NAS\photo\PhotoLibrary"
    duplicates = find_duplicate_images(directory)

    if duplicates:
        print("Duplicate images found:")
        for img_hash, files in duplicates.items():
            print(f"Hash: {img_hash}")
            print("Files:")
            for file in files:
                print(f"Deleting - {file}")
                os.remove(file)
    else:
        print("No duplicate images found.")

if __name__ == "__main__":
    main()
