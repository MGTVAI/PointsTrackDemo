import numpy as np
import sys

LINE_ITEMS_LEN = 5
COORDS_LEN = 8

LINE_ERROR_STR = "行的格式不正确，正确格式如: " \
                 "\n\"n x1,y1 x2,y2, x3,y3 x4,y4\"\n" \
                 "[备注：所有项都应该是数字格式]\n"
NUM_FRAMES_ERROR_STR = "提供的结果文件帧数目与视频帧数不一致，请检查"
FRAME_IDX_ERROR_STR = "行号需与帧序号一致"

def readfile(filename):
    coords_list = []
    with open(filename, 'r') as fr:
        lines = fr.readlines()
        for idx, line in enumerate(lines):
            frame_idx, coords = readline(line)
            if idx != frame_idx:
                raise Exception(FRAME_IDX_ERROR_STR)
            coords_list.append(coords)
    coords_array = np.array(coords_list)
    return coords_array


def readline(line):
    items = line.strip('\n').split()
    # print(len(items))
    if len(items) != LINE_ITEMS_LEN:
        raise Exception(LINE_ERROR_STR)
    frame_idx = int(items[0])
    try:
        points = [tuple([float(i) for i in xy_str.split(',')]) for xy_str in items[1:]]
        points = np.array(points).reshape((-1, ))
        if len(points) != COORDS_LEN:
            raise Exception("需要确保每行只有四点")
    except Exception as e:
        raise Exception(LINE_ERROR_STR)
    return frame_idx, points


def calc_mse(coords_1, coords_2):
    if coords_1.shape != coords_2.shape:
        raise Exception(NUM_FRAMES_ERROR_STR)
    if coords_1.shape[0] < 1:
        raise Exception()
    mse = np.square(coords_1 - coords_2).mean() * 2
    return mse


def main():
    filepath1 = sys.argv[1]
    filepath2 = sys.argv[2]
    coords1 = readfile(filepath1)
    coords2 = readfile(filepath2)
    print(calc_mse(coords1, coords2))


if __name__ == "__main__":
    main()
