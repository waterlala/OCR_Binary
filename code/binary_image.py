import cv2 as cv
import numpy as np
import pandas as pd

#切割大小
CUT_SIZE = 20

#白色膨脹大小
DILATE_SIZE = 41

#雜訊閥值
NOISE_THRESHOLD = 0.9

class BinaryImage:
    def __init__(self, input_image):
        self.image = input_image

    def fit(self):
        """處理"""
        
        imgb_word = np.zeros(self.image.shape, self.image.dtype)

        img_df = self.cut_image(self.image, CUT_SIZE)
        for i in range(len(img_df)):
            single_image = img_df.loc[i]['image']
            start_x = img_df.loc[i]['start_x']
            start_y = img_df.loc[i]['start_y']
            end_x = img_df.loc[i]['end_x']
            end_y = img_df.loc[i]['end_y']
            bgmean = self.get_background_threshold(single_image)
            imgb_word[start_y:end_y, start_x:end_x] = cv.threshold(
                self.image[start_y:end_y, start_x:end_x], int(bgmean * NOISE_THRESHOLD),
                255, cv.THRESH_BINARY)[1]
        return imgb_word

    def get_background_threshold(self, single_local):
        """計算閥值"""

        img_background = cv.dilate(
            np.uint8(single_local),
            np.ones((DILATE_SIZE, DILATE_SIZE), np.uint8))
        backgroundmean = np.mean(img_background)
        backgroundstd = np.std(img_background)
        if backgroundmean >= 175:
            background_threshold = backgroundmean * (0.925 -
                                                     backgroundstd / 95)
        elif backgroundmean < 175 and backgroundmean >= 120:
            background_threshold = backgroundmean * (
                0.9 - (175 - backgroundmean) * 0.00095 - backgroundstd / 95)  #
        else:
            background_threshold = backgroundmean * (0.85 - backgroundstd / 95
                                                     )  #
        return background_threshold

    def cut_image(self, input_image, input_range):
        """切割圖片"""

        image_df = pd.DataFrame(
            columns=['image', 'start_x', 'end_x', 'start_y', 'end_y'])
        for i in range(input_range):
            start_x = int(0 + i * (input_image.shape[1] / input_range))
            end_x = int((i + 1) * (input_image.shape[1] / input_range))
            for j in range(input_range):
                start_y = int(0 + j * (input_image.shape[0] / input_range))
                end_y = int((j + 1) * (input_image.shape[0] / input_range))
                single_image = input_image[start_y:end_y, start_x:end_x]
                image_df.loc[len(image_df)] = [
                    single_image, start_x, end_x, start_y, end_y
                ]
        return image_df