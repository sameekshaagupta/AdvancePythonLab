from PIL import Image, ImageFilter, ImageEnhance
import matplotlib.pyplot as plt
import os
import numpy as np
def load_image(image_path):
    try:
        img = Image.open(image_path)
        return img
    except Exception as e:
        print(f"Error: {e}")
        return None
        
def display_image(img):
    plt.imshow(img)
    plt.axis('off')
    plt.show()

def apply_gaussian_blur(img, radius):
    return img.filter(ImageFilter.GaussianBlur(radius))

def convert_to_grayscale(img):
    return img.convert("L")
def resize_image(img, new_width, new_height):
    return img.resize((new_width, new_height))

def crop_image(img, left, top, right, bottom):
    return img.crop((left, top, right, bottom))

def adjust_brightness(img, factor):
    enhancer = ImageEnhance.Brightness(img)
    return enhancer.enhance(factor)

def adjust_contrast(img, factor):
    enhancer = ImageEnhance.Contrast(img)
    return enhancer.enhance(factor)

def adjust_saturation(img, factor):
    enhancer = ImageEnhance.Color(img)
    return enhancer.enhance(factor)

def plot_histogram(img):
    # Split the image into its respective color channels
    r, g, b = img.split()
    
    # Convert channels to numpy arrays
    r_array = np.array(r)
    g_array = np.array(g)
    b_array = np.array(b)
    
    # Plot histograms for each channel
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 3, 1)
    plt.hist(r_array.ravel(), bins=256, color='red', alpha=0.5)
    plt.title('Red Channel Histogram')
    
    plt.subplot(1, 3, 2)
    plt.hist(g_array.ravel(), bins=256, color='green', alpha=0.5)
    plt.title('Green Channel Histogram')
    
    plt.subplot(1, 3, 3)
    plt.hist(b_array.ravel(), bins=256, color='blue', alpha=0.5)
    plt.title('Blue Channel Histogram')
    
    plt.show()

def main():
    data_folder = r'photo'
    image_path = os.path.join(data_folder, 'photo.jpg')
    img=load_image(image_path)
    
    if img is not None:
        while True:
            print("\nChoose an operation:")
            print("1. Display the original image")
            print("2. Apply Gaussian blur")
            print("3. Convert to grayscale")
            print("4. Resize the image")
            print("5. Crop the image")
            print("6. Adjust brightness")
            print("7. Adjust contrast")
            print("8. Adjust saturation")
            print("9. Display histograms")
            print("10. Exit")
            
            choice = input("Enter your choice (1-10): ")
            
            if choice == "1":
                display_image(img)
            elif choice == "2":
                radius = float(input("Enter the blur radius: "))
                blurred_img = apply_gaussian_blur(img, radius)
                display_image(blurred_img)
            elif choice == "3":
                grayscale_img = convert_to_grayscale(img)
                display_image(grayscale_img)
            elif choice == "4":
                new_width = int(input("Enter new width: "))
                new_height = int(input("Enter new height: "))
                resized_img = resize_image(img, new_width, new_height)
                display_image(resized_img)
            elif choice == "5":
                left = int(input("Enter left coordinate: "))
                top = int(input("Enter top coordinate: "))
                right = int(input("Enter right coordinate: "))
                bottom = int(input("Enter bottom coordinate: "))
                cropped_img = crop_image(img, left, top, right, bottom)
                display_image(cropped_img)
            elif choice == "6":
                factor = float(input("Enter brightness factor (1.0 for no change): "))
                bright_img = adjust_brightness(img, factor)
                display_image(bright_img)
            elif choice == "7":
                factor = float(input("Enter contrast factor (1.0 for no change): "))
                contrast_img = adjust_contrast(img, factor)
                display_image(contrast_img)
            elif choice == "8":
                factor = float(input("Enter saturation factor (1.0 for no change): "))
                saturated_img = adjust_saturation(img, factor)
                display_image(saturated_img)
            elif choice == "9":
                plot_histogram(img)
            elif choice == "10":
                print("Exiting...")
                break
            else:
                print("Invalid choice, please try again.")
    else:
        print("Failed to load image. Exiting...")

if __name__ == "__main__":
    main()
