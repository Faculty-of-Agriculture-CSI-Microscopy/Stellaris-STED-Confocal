from readlif.reader import LifFile
import os

def read_lif_file(file_path):
    print(f"Checking file path: {file_path}")
    if not os.path.exists(file_path):
        print("File not found!")
        return

    try:
        lif_file = LifFile(file_path)
        print("File Information:")

        for image in lif_file.get_iter_image():
            print(f"Image Name: {image.name}")
            print(f"Dimensions: {image.dims}")
            print(f"Number of Z frames: {image.nz}")
            print(f"Number of T frames: {image.nt}")
            print(f"Number of Channels: {image.channels}")
            print("-" * 40)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    file_path = input("Please enter the full path to the .lif file (including the file name): ").strip().strip('"')
    read_lif_file(file_path)
