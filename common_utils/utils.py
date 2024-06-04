import cv2 as cv
import json
import os


def verif_path(p):
    if not os.path.exists(p):
        os.makedirs(p)


def list_folders(path):
    return [f_ for f_ in os.listdir(path) if os.path.isdir(os.path.join(path, f_))]


def list_files(path, file_extension=None):
    if file_extension is None:
        return [f_ for f_ in os.listdir(path) if os.path.isfile(os.path.join(path, f_))]
    else:
        return [f_ for f_ in os.listdir(path) if os.path.splitext(f_)[1] == file_extension]


def imshow_and_wait(img, window_name="Image"):
    cv.imshow(window_name, img)
    cv.waitKey(0)
    cv.destroyWindow(window_name)


def load_json(load_path):
    return json.load(open(load_path, "r"))


def save_json(data, save_path):
    with open(save_path, "w") as save_file:
        json.dump(data, save_file, ensure_ascii=True, indent=4)
