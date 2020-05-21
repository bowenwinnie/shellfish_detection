from matplotlib import pyplot as plt
from clodsa.augmentors.augmentorFactory import createAugmentor
from clodsa.transformers.transformerFactory import transformerGenerator
from clodsa.techniques.techniqueFactory import createTechnique
import cv2
import numpy as np
import skimage.io as io
import matplotlib.pyplot as plt
import pylab
from pycocotools.coco import COCO

PROBLEM = "instance_segmentation"
ANNOTATION_MODE = "coco"
INPUT_PATH = "/Users/sunbowen/Desktop/shellfish_detection/data/val_img"
GENERATION_MODE = "linear"
OUTPUT_MODE = "coco"
OUTPUT_PATH = "/Users/sunbowen/Desktop/shellfish_detection/data/output/"

augmentor = createAugmentor(PROBLEM, ANNOTATION_MODE, OUTPUT_MODE, GENERATION_MODE, INPUT_PATH, {"outputPath": OUTPUT_PATH})
transformer = transformerGenerator(PROBLEM)

# Rotations
for angle in [0, 90, 180]:
    rotate = createTechnique("rotate", {"angle": angle})
    augmentor.addTransformer(transformer(rotate))

# Flip
flip = createTechnique("flip", {"flip": 1})
augmentor.addTransformer(transformer(flip))

# Implementation
augmentor.applyAugmentation()
#
# image_directory = OUTPUT_PATH
# annotation_file = OUTPUT_PATH + 'annotation.json'
#
# example_coco = COCO(annotation_file)
#
# categories = example_coco.loadCats(example_coco.getCatIds())
# category_names = [category['name'] for category in categories]
# print('Custom COCO categories: \n{}\n'.format(' '.join(category_names)))
#
# category_names = set([category['supercategory'] for category in categories])
# print('Custom COCO supercategories: \n{}'.format(' '.join(category_names)))
#
# category_ids = example_coco.getCatIds(catNms=['circle'])
# image_ids = example_coco.getImgIds(catIds=category_ids)
# image_data = example_coco.loadImgs(image_ids[np.random.randint(0, len(image_ids))])[0]

