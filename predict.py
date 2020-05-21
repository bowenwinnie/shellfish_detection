# import some common detectron2 utilities
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.logger import setup_logger
from detectron2.utils.visualizer import Visualizer, ColorMode
from matplotlib import pyplot as plt
from detectron2.data.detection_utils import read_image
import cv2
import json
import os
import multiprocessing as mp
import os
import time
import glob
import tqdm
from detectron2.data import DatasetCatalog, MetadataCatalog
from detectron2.data.datasets import register_coco_instances
import argparse

dir_path = os.path.dirname(os.path.abspath(__file__))

print('root' + dir_path)
WINDOW_NAME = "Shellfish Counting"

# get image
TRAIN_JSON = dir_path + "/data/aug_val/annotation.json"
TRAIN_PATH = dir_path + "/data/aug_val"
# MODEL_WEIGHTS = "/Users/sunbowen/Desktop/shellfish_detection/data/logs/model_final.pth"
MODEL_WEIGHTS = dir_path + "/output/model_final.pth"

def setup_cfg(args):
    # load config from file and command-line arguments
    # # Create config
    cfg = get_cfg()
    cfg.MODEL.DEVICE = 'cpu'
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    # Set score_threshold for builtin models
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = args.confidence_threshold
    cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = args.confidence_threshold
    cfg.MODEL.WEIGHTS = MODEL_WEIGHTS
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = 3

    cfg.freeze()
    return cfg


def get_parser():
    parser = argparse.ArgumentParser(description="Detectron2")
    parser.add_argument(
        "--config-file",
        default=dir_path + "/detectron2-repo/configs/COCO-InstanceSegmentation/mask_rcnn_R_101_FPN_3x.yaml",
        metavar="FILE",
        help="path to config file",
    )
    parser.add_argument(
        "--input",
        nargs="+",
        help="A list of space separated input images; "
        "or a single glob pattern such as 'directory/*.jpg'",
    )
    parser.add_argument(
        "--output",
        # default="data/logs",
        help="A file or directory to save output visualizations. "
        "If not given, will show output in an OpenCV window.",
    )
    parser.add_argument(
        "--confidence-threshold",
        type=float,
        default=0.7,
        help="Minimum score for instance predictions to be shown",
    )
    parser.add_argument(
        "--opts",
        help="Modify config options using the command-line 'KEY VALUE' pairs",
        default=[],
        nargs=argparse.REMAINDER,
    )
    parser.add_argument(
        "--web",
        help="Call the script from web application. web: 1",
        default=0,
    )
    return parser


if __name__ == "__main__":
    mp.set_start_method("spawn", force=True)
    args = get_parser().parse_args()
    # setup_logger(name="fvcore")
    # logger = setup_logger()
    # logger.info("Arguments: " + str(args))

    cfg = setup_cfg(args)

    # register dataset
    register_coco_instances("shellfish", {}, TRAIN_JSON, TRAIN_PATH)
    shellfish_metadata = MetadataCatalog.get("shellfish")
    dataset_dicts = DatasetCatalog.get("shellfish")

    if args.input:
        if len(args.input) == 1:
            args.input = glob.glob(os.path.expanduser(args.input[0]))
            assert args.input, "The input path(s) was not found"
        for path in tqdm.tqdm(args.input, disable=not args.output):
            # use PIL, to be consistent with evaluation
            img = read_image(path, format="BGR")
            start_time = time.time()
            predictor = DefaultPredictor(cfg)
            outputs = predictor(img)

            # logger.info(
            #     "{}: {} in {:.2f}s".format(
            #         path,
            #         "detected {} instances".format(len(outputs["instances"]))
            #         if "instances" in outputs
            #         else "finished",
            #         time.time() - start_time,
            #     )
            # )
            print("{}: {} in {:.2f}s".format(
                path,
                "detected {} instances".format(len(outputs["instances"]))
                if "instances" in outputs
                else "finished",
                time.time() - start_time,
                ))
            v = Visualizer(img[:, :, ::-1], metadata=shellfish_metadata, scale=1, instance_mode=ColorMode.IMAGE_BW)
            v = v.draw_instance_predictions(outputs["instances"].to("cpu"))

            # Save predicted image in output folder if path specified
            if args.output:
                if os.path.isdir(args.output):
                    assert os.path.isdir(args.output), args.output
                    out_filename = os.path.join(args.output, os.path.basename(path))
                    v.save(out_filename)
                    # im_cv = cv2.imread(out_filename)
                    # im_rgb = cv2.cvtColor(im_cv, cv2.COLOR_BGR2RGB)
                    # if args.web == 1:
                    # print(out_filename)

                # Visualize predicted image
            else:
                cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
                cv2.imshow(WINDOW_NAME, v.get_image()[:, :, ::-1])
                if cv2.waitKey(0) == 27:
                    break  # esc to quit

                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
