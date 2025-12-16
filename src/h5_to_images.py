import h5py
import os
import cv2

# ===================== CONFIG =====================
H5_FILE = "../data/food_c101_n1000_r384x384x3.h5"# adjust if file is elsewhere
OUTPUT_DIR = "../data/subset_100"
MAX_IMAGES = 100   # reduce to 200 or 500 if needed
# =================================================

def convert_h5_to_images():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with h5py.File(H5_FILE, "r") as f:
        print("H5 keys:", list(f.keys()))

        images = f["images"][:]   # (N, H, W, 3)
        total = images.shape[0]
        print(f"Total images found: {total}")

        count = min(MAX_IMAGES, total)

        for i in range(count):
            img = images[i]

            # Convert RGB → BGR for OpenCV
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            filename = os.path.join(OUTPUT_DIR, f"img_{i:04d}.jpg")
            cv2.imwrite(filename, img)

            if i % 100 == 0:
                print(f"Saved {i}/{count}")

    print("\n✅ Conversion complete!")
    print(f"Images saved in: {OUTPUT_DIR}")

if __name__ == "__main__":
    convert_h5_to_images()
