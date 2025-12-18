import h5py
import os
import cv2

# ===================== CONFIG =====================
H5_FILE = "../data/food_test_c101_n1000_r128x128x1.h5"
OUTPUT_DIR = "../data/subset_5000"
MAX_IMAGES = 5000   
# =================================================

def convert_h5_to_images():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with h5py.File(H5_FILE, "r") as f:

        images = f["images"][:]   # (N, H, W, 3)
        total = images.shape[0]
        print(f"Total images found: {total}")

        count = min(MAX_IMAGES, total)

        for i in range(count):
            img = images[i]

            # Convert RGB to BGR for OpenCV
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            filename = os.path.join(OUTPUT_DIR, f"img_{i:04d}.jpg")
            cv2.imwrite(filename, img)

            if i % 100 == 0:
                print(f"Saved {i}/{count}")

    print("Conversion complete.")
    print(f"Images saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    convert_h5_to_images()

