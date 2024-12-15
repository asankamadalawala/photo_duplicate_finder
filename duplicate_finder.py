import os
from PIL import Image
import imagehash
import pillow_heif

# Register HEIF plugin for Pillow
pillow_heif.register_heif_opener()

def find_and_delete_duplicates(directory):
    """
    Find and delete duplicate images in a directory based on perceptual hashing.

    :param directory: Path to the directory containing images.
    """
    hash_dict = {}  # Dictionary to store unique hashes and their file paths
    duplicates = []  # List to store duplicate file paths

    print("checking...", end="")
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with Image.open(file_path) as img:
                    # Generate perceptual hash
                    img_hash = imagehash.phash(img)

                # Check for duplicates
                if img_hash in hash_dict:
                    # If hash exists, mark this file as a duplicate
                    duplicates.append(file_path)
                    print("+",end="")
                else:
                    # Otherwise, add the hash and file path to the dictionary
                    hash_dict[img_hash] = file_path
                    print(".",end="")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

    # Delete duplicate files
    for duplicate_file in duplicates:
        try:
            os.remove(duplicate_file)
            print(f"Deleted duplicate: {duplicate_file}")
        except Exception as e:
            print(f"Error deleting {duplicate_file}: {e}")

    print(f"Total duplicates found and deleted: {len(duplicates)}")

def main():
    directory = r"D:\Images"  # Replace with your directory path
    find_and_delete_duplicates(directory)

if __name__ == "__main__":
    main()
