from PIL import Image
import matplotlib.pyplot as plt
def load_and_display_image(image_path):
    image = Image.open(image_path)

    plt.imshow(image)
    plt.axis('off')
    plt.show()

image_path = '3\\task1\hello.jpg'
load_and_display_image(image_path)