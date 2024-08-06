from PIL import ImageFilter, Image
import matplotlib.pyplot as plt

def apply_filters(image):
    blurred_image = image.filter(ImageFilter.GaussianBlur(radius=5))
    
    edges_image = image.filter(ImageFilter.FIND_EDGES)
    
    return blurred_image, edges_image

def resize_and_crop(image, new_size=(800, 600), crop_box=(100, 100, 700, 500)):
    # Resize the image
    resized_image = image.resize(new_size)
    
    # Crop the image
    cropped_image = image.crop(crop_box)
    
    return resized_image, cropped_image

# Example usage
image = Image.open('3\\task2\photo.jpg')
blurred_image, edges_image = apply_filters(image)
resized_image, cropped_image = resize_and_crop(image)

# Display manipulated images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(blurred_image)
plt.title('Blurred Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(edges_image)
plt.title('Edges Image')
plt.axis('off')
plt.show()
