import cv2 as cv
import json
import os


def verif_path(p):
    if not os.path.exists(p):
        os.makedirs(p)


def list_folders(path, reverse_sort=False):
    return sorted([f_ for f_ in os.listdir(path) if os.path.isdir(os.path.join(path, f_))], reverse=reverse_sort)


def list_files(path, reverse_sort=False, file_extension=None, keep_path=False):
    if file_extension is None:
        files = [f_ for f_ in os.listdir(path) if os.path.isfile(os.path.join(path, f_))]
    else:
        files = [f_ for f_ in os.listdir(path) if os.path.splitext(f_)[1] == file_extension]

    files.sort(reverse=reverse_sort)

    return [os.path.join(path, f_) for f_ in files] if keep_path else files


def list_files_recursively(start_path):
    files = []
    for root, dirs, files in os.walk(start_path):
        files += [os.path.join(root, file) for file in files]
    return files


def imshow_and_wait(img, window_name="imshow", window_x=0, window_y=0):
    cv.imshow(window_name, img)
    cv.moveWindow(window_name, window_x, window_y)
    cv.waitKey(0)
    if cv.getWindowProperty(window_name, cv.WND_PROP_VISIBLE):
        cv.destroyWindow(window_name)


def image_resize(image, width=None, height=None, inter=cv.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def load_json(load_path):
    return json.load(open(load_path, "r"))


def save_json(data, save_path):
    with open(save_path, "w") as save_file:
        json.dump(data, save_file, ensure_ascii=True, indent=4)


def append_json(data, save_path):
    previous_data = load_json(save_path)
    previous_data.update(data)
    save_json(previous_data, save_path)


def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=lambda i: seq[i])


def sort_by(seq, sort_key):
    return [seq[idx] for idx in argsort(sort_key)]
