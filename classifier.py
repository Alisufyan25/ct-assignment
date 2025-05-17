import cv2
import numpy as np
import os

print(" Name: Ali Sufyan \n Enrollment 02-235232-017\n ")
def load_image(path):
    image = cv2.imread(path)
    if image is None:
        raise ValueError(f"Image not found at path: {path}")
    return image

def analyze_image(image):
    resized = cv2.resize(image, (100, 100))
    hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    avg_brightness = np.mean(gray)
    black_pixels = np.sum(gray < 50)
    colorful_pixels = np.sum((hsv[:, :, 1] > 80) & (hsv[:, :, 2] > 80))
    total_pixels = resized.shape[0] * resized.shape[1]
    return avg_brightness, black_pixels / total_pixels, colorful_pixels / total_pixels
def assign_belt(avg_brightness, black_ratio, colorful_ratio):
    if avg_brightness > 180 and colorful_ratio < 0.1:
        return 'B'  # Transparent
    elif black_ratio > 0.5:
        return 'A'  # Black
    elif colorful_ratio > 0.3:
        return 'C'  # Colorful
    else:
        return 'Unknown'
results = []
def process_image(image_path):
    try:
        image = load_image(image_path)
        avg_brightness, black_ratio, colorful_ratio = analyze_image(image)
        belt = assign_belt(avg_brightness, black_ratio, colorful_ratio)
        results.append({
            "filename": os.path.basename(image_path),
            "brightness": avg_brightness,
            "black_ratio": black_ratio,
            "colorful_ratio": colorful_ratio,
            "belt": belt
        })
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
def process_all_images(dataset_path):
    for category in ['black', 'transparent', 'colorful']:
        folder_path = os.path.join(dataset_path, category)
        if not os.path.exists(folder_path):
            print(f"Folder not found: {folder_path}")
            continue
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                image_path = os.path.join(folder_path, filename)
                process_image(image_path)

def print_results():
    print("\n--- Image Classification Report ---")
    print(f"{'Image':<25} {'Brightness':<12} {'Black %':<10} {'Colorful %':<12} {'Belt'}")
    print("-" * 65)
    for r in results:
        print(f"{r['filename']:<25} "
              f"{r['brightness']:<12.2f} "
              f"{r['black_ratio']*100:<10.2f} "
              f"{r['colorful_ratio']*100:<12.2f} "
              f"{r['belt']}")

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())

    dataset_path = "dataset"
    if not os.path.exists(dataset_path):
        print(f"Dataset folder not found at: {dataset_path}")
    else:
        folders = os.listdir(dataset_path)
        print("\nFolders inside dataset:")
        for f in folders:
            print(f"  - {f}")

    process_all_images(dataset_path)
    print_results()
    #next line 
print(" \nEnd of processing")
