import numpy as np
from aicsimageio.writers import OmeTiffWriter
from readlif.reader import LifFile
import os

def read_lif_file(file_path):
    try:
        lif_file = LifFile(file_path)
        images = []
        for image in lif_file.get_iter_image():
            frames = [np.array(frame) for frame in image.get_iter_t()]
            metadata = {
                'Name': image.name,
                'Dimensions': image.dims,
                'Number of Z frames': image.nz,
                'Number of T frames': image.nt,
                'Number of Channels': image.channels,
                'Size': sum(frame.nbytes for frame in frames) / 1e6  # Approximate size in MB
            }
            images.append((frames, metadata))
        return images
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def create_projection(frames, projection_type="Max"):
    frames_array = np.stack(frames, axis=0)  # Stack frames into a single NumPy array
    if projection_type == "Max":
        return np.max(frames_array, axis=0)
    elif projection_type == "Average":
        return np.mean(frames_array, axis=0)
    elif projection_type == "Sum":
        return np.sum(frames_array, axis=0)
    elif projection_type == "Standard Deviation":
        return np.std(frames_array, axis=0)
    elif projection_type == "None":
        return frames_array
    else:
        raise ValueError(f"Unknown projection type: {projection_type}")

def convert_lif_to_ome_tiff(file_path, output_folder, projection_type="Max"):
    dataset = read_lif_file(file_path)
    if dataset is None:
        print("Failed to load dataset.")
        return

    if output_folder.endswith('"'):
        output_folder = output_folder[:-1]

    for i, (frames, metadata) in enumerate(dataset):
        projection = create_projection(frames, projection_type)
        output_path = os.path.join(output_folder, f"{metadata['Name']}.ome.tiff")
        print(f"Saving {output_path}")
        dim_order = 'ZYX' if projection.ndim == 3 else 'YXC' if projection.ndim == 4 else 'YX'
        OmeTiffWriter.save(projection, output_path, dim_order=dim_order)
        print(f"Saved {output_path}")

if __name__ == "__main__":
    file_path = input("Please enter the full path to the .lif file: ").strip().strip('"')
    output_folder = input("Please enter the output folder path: ").strip().strip('"')
    projection_type = input("Please enter the projection type (Max, Average, Sum, Standard Deviation, None): ").strip().capitalize()

    convert_lif_to_ome_tiff(file_path, output_folder, projection_type)
