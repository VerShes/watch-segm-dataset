import os
import matplotlib.pyplot as plt
import shutil
from PIL import Image


class ImageMaskViewer:
    def __init__(self, image_folder: str, mask_folder: str, path_cache: str = None):
        self.image_folder = image_folder
        self.mask_folder = mask_folder
        self.images = sorted([f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))])
        self.masks = sorted([f for f in os.listdir(mask_folder) if os.path.isfile(os.path.join(mask_folder, f))])
        self.path_cache = path_cache
        self.index = 0

        if self.path_cache:
            self.path_image_cache = os.path.join(self.path_cache, 'images')
            self.path_mask_cache = os.path.join(self.path_cache, 'masks')
            if not os.path.exists(self.path_image_cache):
                os.mkdir(self.path_image_cache)
            if not os.path.exists(self.path_mask_cache):
                os.mkdir(self.path_mask_cache)

        assert len(self.images) == len(self.masks), "Count of images and masks don't match"

        self.fig, self.axes = plt.subplots(1, 2, figsize=(10, 5))
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.update_display()

    def update_display(self):
        self.axes[0].clear()
        self.axes[1].clear()

        image_path = os.path.join(self.image_folder, self.images[self.index])
        mask_path = os.path.join(self.mask_folder, self.masks[self.index])

        image = Image.open(image_path)
        mask = Image.open(mask_path)

        self.axes[0].imshow(image)
        self.axes[0].set_title('Image')
        self.axes[0].axis('off')

        self.axes[1].imshow(mask)
        self.axes[1].set_title('Mask')
        self.axes[1].axis('off')

        self.fig.canvas.draw()

    def on_key(self, event):
        if event.key == 'right':
            self.index = (self.index + 1) % len(self.images)
        elif event.key == 'left':
            self.index = (self.index - 1) % len(self.images)
        elif event.key == ' ':
            if self.path_cache:
                shutil.copy2(os.path.join(self.image_folder, self.images[self.index]),
                             os.path.join(self.path_image_cache, self.images[self.index]))
                shutil.copy2(os.path.join(self.mask_folder, self.masks[self.index]),
                             os.path.join(self.path_mask_cache, self.masks[self.index]))
                os.remove(os.path.join(self.image_folder, self.images[self.index]))
                os.remove(os.path.join(self.mask_folder, self.masks[self.index]))
            else:
                os.remove(os.path.join(self.image_folder, self.images[self.index]))
                os.remove(os.path.join(self.mask_folder, self.masks[self.index]))
            del self.images[self.index]
            del self.masks[self.index]
            self.index = self.index % len(self.images)
        if self.images and self.masks:
            self.update_display()
        else:
            print("All images and masks are deleted")
            plt.close(self.fig)

    def run(self):
        plt.show()


if __name__ == "__main__":
    image_folder = r'D:\Data Science\resized_dataset\image'
    mask_folder = r'D:\Data Science\resized_dataset\mask'
    path_cache = r'D:\Data Science\resized_dataset\cache'
    viewer = ImageMaskViewer(image_folder, mask_folder, path_cache)
    viewer.run()
