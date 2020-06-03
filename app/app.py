import streamlit as st
import numpy as np
import torch
from PIL import Image
import os
from collections import Counter
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer, ColorMode
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.engine import DefaultPredictor
from detectron2 import model_zoo


# Define the target shellfish classes
target_classes = ['cockle', 'mussel', 'tuatua']

MODEL_WEIGHTS = "model/model_final.pth"
# Remove dropdown menu
hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


def setup_cfg():
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_101_FPN_3x.yaml"))
    # cfg.merge_from_file("/Users/sunbowen/Desktop/shellfish_detection/app/model/final_mask_rcnn_R_101_FPN_3x.yaml")
    cfg.MODEL.DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    cfg.MODEL.WEIGHTS = MODEL_WEIGHTS

    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = 0.7

    cfg.DATASETS.TEST = ("shellfish",)
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3

    cfg.DATALOADER.NUM_WORKERS = 2
    cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128

    cfg.SOLVER.IMS_PER_BATCH = 2
    cfg.SOLVER.BASE_LR = 0.001
    cfg.SOLVER.MAX_ITER = 10000

    # cfg.freeze()
    return cfg


class ShellfishVisualizer(Visualizer):
    # Draw shellfish classes and count on images
    def draw_class_count(self, predictions):
        classes = predictions.pred_classes if predictions.has("pred_classes") else None
        class_names = self.metadata.get("thing_classes", None)
        if classes is not None and class_names is not None and len(class_names) > 1:
            labels = [class_names[i] for i in classes]
            counts = Counter(labels)
            text_string = ''
            x = self.output.height * 0.02
            y = self.output.width * 0.02
            for key in counts:
                text_string += str(key) + ': ' + str(counts[key]) + ' ' if text_string == '' else '\n' + str(
                    key) + ': ' + str(counts[key]) + ' '

            self.draw_text(text_string, (x, y), horizontal_alignment='left', color='green')


def run_inference(img):
    # Setup model config
    cfg = setup_cfg()

    shellfish_metadata = MetadataCatalog.get(cfg.DATASETS.TEST[0]).set(thing_classes=target_classes)

    # Create predictor
    predictor = DefaultPredictor(cfg)
    outputs = predictor(img)

    v = ShellfishVisualizer(img[:, :, ::-1],
                            metadata=shellfish_metadata,
                            scale=1,
                            instance_mode=ColorMode.IMAGE)

    # Draw shellfish classes and counts on the top left of the image
    v.draw_class_count(outputs["instances"].to("cpu"))

    # Draw predicted bounding boxes and masks
    visualized = v.draw_instance_predictions(outputs["instances"].to("cpu"))

    return visualized.get_image(), outputs['instances']


def main():
    st.title("Shellfish Detection and Counting")
    st.write("## Upload image")

    uploaded_image = st.file_uploader("Please choose a png or jpg image", type=["jpg", "png", "jpeg"])

    if uploaded_image is not None:
        # use PIL, to be consistent with evaluation
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
        # Convert image and color channel to RGB
        image = image.convert("RGB")
        img = np.asarray(image)
        # Revert color channel to RGB
        img = img[:, :, ::-1]

        if st.button("Detect and Count"):
            with st.spinner("Processing..."):
                # Setup config
                predicted_img, instances = run_inference(img)

                # Get and print predicted classes
                classes = np.array(instances.pred_classes)
                predicted_classes = [target_classes[i] for i in classes]
                st.markdown('<style>p{color:#8A2BE2}</style>', unsafe_allow_html=True)
                st.write("Detected Shellfish:")

                message = ''
                for (key, value) in Counter(predicted_classes).items():
                    message += str(key) + ': ' + str(value) if message == '' else ', ' + str(key) + ': ' + str(value)

                st.write('*' + message + '*')

                st.image(predicted_img, caption="Result", use_column_width=True)


if __name__ == "__main__":
    main()
