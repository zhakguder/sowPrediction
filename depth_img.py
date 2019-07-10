import csv
import fnmatch
import numpy as np
import matplotlib.pyplot as plt
from os import makedirs, sep, listdir, path
from sys import argv
from pdb import set_trace

class DepthData:

    def __init__(self, path_to_depth_txts):
        self.text_folder = path_to_depth_txts
        self.base_path = self.text_folder.split(sep)[:-1]

    def _image_folder_name(self, img_folder_ext):
        self.image_folder = sep.join(self.base_path + [img_folder_ext])
        return self.image_folder

    def _create_image_folder(self, img_folder_ext):
        image_folder = self._image_folder_name(img_folder_ext)
        self.image_folder = image_folder
        try:
            makedirs(image_folder)

        except:
            pass

        return self.image_folder

    def _list_image_names(self):
        image_text_files = fnmatch.filter(listdir(self.text_folder), '*.txt')
        return image_text_files

    def create_image_spreadsheet(self):
        names = self._list_image_names()
        with open(path.join(sep.join(self.base_path), 'depth_labels.csv'), 'w') as writeFile:
            writer = csv.writer(writeFile, delimiter=',')
            for name in names:
                writer.writerow([name])

    def _create_image(self, text_name, image_name):
        x = np.genfromtxt(text_name, dtype=int, delimiter=',')
        plt.imshow(x)
        plt.savefig(image_name)

    def create_images(self, img_folder_ext):
        image_folder = self._create_image_folder(img_folder_ext)
        text_names = self._list_image_names()
        image_names = ['{}.png'.format(path.splitext(name)[0]) for name in text_names]
        for text_name, image_name in zip(text_names, image_names):
            text_path = path.join(self.text_folder, text_name)
            image_path = path.join(image_folder, image_name)
            if not path.exists(image_path):
                self._create_image(text_path, image_path)


if __name__ == '__main__':
    image_data = DepthData(argv[1])
    image_data.create_image_spreadsheet()
    image_data.create_images('depth_imgs')
