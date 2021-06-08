from PIL import PpmImagePlugin
# 型をつけるため
from pdf2image import convert_from_path
# pdfをimageに変換
import numpy as np
# numpy
import cv2
# openCV

pdf_path = 'pdf/test.pdf'

def main():
    pdfs = convert_from_path(pdf_path)
    # pdfをimageに変換

    for page in range(len(pdfs)):
        img: PpmImagePlugin.PpmImageFile = pdfs[page]
        grayscale_img_as_arr = convert_gray(img)
        # グレースケールに変換
        line_list = get_line_list(grayscale_img_as_arr)
        # 線があるy座標のリスト
        line_list = bundle_line(line_list)
        # 線がいつくかのy軸をまたいでしまってる。故にばらつきをなくす
        output_divided_img(page,line_list,grayscale_img_as_arr)
        # 出力

def convert_gray(img):
    img_as_arr= np.asarray(img)
    # 画像をnumpy形式に変換
    return cv2.cvtColor(img_as_arr, cv2.COLOR_BGR2GRAY)
    # RGB→グレースケールに変換(白黒のグラデーションは残ってる。昔の写真見たいな)

def get_line_list(grayscale_img_as_arr):
    line_list = []
    white_num = 255
    # y軸
    for y in range(len(grayscale_img_as_arr)):
        line_length_list = []
        # x軸
        line_length = 0
        for x in range(len(grayscale_img_as_arr[y])):
            if grayscale_img_as_arr[y][x] < white_num:
                line_length += 1
            else:
                line_length = 0
            line_length_list.append(line_length)

        line_length_list.sort()
        max_length = line_length_list[-1]

        # 黒が300以上続いてたら線と認定する
        if max_length  > 300:
            line_list.append(y)

    return line_list

def bundle_line(line_list):
    bundled_line_list = []
    # 線とする場所
    for i in range(len(line_list)):
        if i == 0:
            bundled_line_list.append(line_list[i])
        if line_list[i] - bundled_line_list[-1] > 50:
            # line_list[i]が現在のループ
            # bundled_line_list[-1]は前回線として認定した場所。
            # それが50より大きかった場合
            bundled_line_list.append(line_list[i])
    return bundled_line_list

def output_divided_img(page,line_list,grayscale_img_as_arr):
    img_width = grayscale_img_as_arr.shape[1]
    for i in range(len(line_list)):
        if i == 0:
            divided_image = grayscale_img_as_arr[0:line_list[i], 0:img_width]
            # 第一引数はY軸,第二引数はX軸。y = 0から1個目の線
        else:
            divided_image = grayscale_img_as_arr[line_list[i-1]:line_list[i], 0:img_width]
            # y = 前回の線から今回の線
        cv2.imwrite(f'result/pdf{page}-{i}.png', divided_image)
        # pngとして出力。

if __name__ == '__main__':
    main()