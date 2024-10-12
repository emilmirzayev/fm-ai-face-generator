"""
Author: Emil Mirzayev

This script removes the background from images in a specified directory and its subfolders.
It processes JPG and JPEG files, converting them to PNG files with transparent backgrounds.
"""

import os
import argparse
from rembg import remove
from PIL import Image
import glob
from tqdm import tqdm



def remove_background(input_path, output_path):
    """
    Remove the background from a single image.

    Args:
    input_path (str): Path to the input image file.
    output_path (str): Path where the processed image will be saved.
    """
    with Image.open(input_path) as img:
        output = remove(img)
        output.save(output_path)

def process_directory(directory):
    """
    Process all JPG and JPEG images in the given directory and its subfolders.

    Args:
    directory (str): Path to the directory containing images.

    Returns:
    int: The number of images successfully processed.
    """
    processed_count = 0
    
    # Get the total number of files to process
    total_files = sum(len(files) for _, _, files in os.walk(directory))
    
    # Create a progress bar
    with tqdm(total=total_files, desc="Processing images", unit="image") as pbar:
        for subdir, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(('.jpg', '.jpeg')):
                    input_path = os.path.join(subdir, file)
                    output_filename = os.path.splitext(file)[0] + '.png'
                    output_path = os.path.join(subdir, output_filename)
                    
                    try:
                        remove_background(input_path, output_path)
                        processed_count += 1
                    except Exception as e:
                        print(f"Error processing {input_path}: {str(e)}")
                
                # Update the progress bar
                pbar.update(1)
    
    return processed_count
def main():
    """
    Main function to parse command-line arguments and initiate the background removal process.
    """
    parser = argparse.ArgumentParser(description="Remove background from images in a directory and its subfolders")
    parser.add_argument("--directory", type=str, default="generated_images", help="Path to the directory containing images. Defaults to `generated_images` folder in the same directory")
    args = parser.parse_args()

    total_processed = process_directory(args.directory)
    print(f"\nTotal images processed: {total_processed}")

if __name__ == "__main__":
    main()
