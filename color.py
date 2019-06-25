import numpy as np
import matplotlib.pyplot as plt
from skimage import io


def color_judge(red_channel, green_channel, blue_channel, color) -> bool:
    """

    :param red_channel:
    :param green_channel:
    :param blue_channel:
    :param color: The color that the user provided in the form
    :return: return True if the RGB values of input images match the color that user provided
    """
    # color match
    # Black
    if color == 1:
        if red_channel < 90 and green_channel < 90 and blue_channel < 90:
            avg = np.mean([red_channel, green_channel, blue_channel])
            if red_channel - avg <= 10 and green_channel - avg <= 10 and blue_channel - avg <= 10:
                return True
        else:
            return False
    # Red
    if color == 2:
        if red_channel - np.mean([green_channel, blue_channel]) >= 50:
            return True
        else:
            return False
    # Green
    if color == 3:
        if green_channel - np.mean([red_channel, blue_channel]) >= 50:
            return True
        else:
            return False
    # Blue
    if color == 4:
        if blue_channel - np.mean([red_channel, green_channel]) >= 50:
            return True
        else:
            return False
    # Yellow
    if color == 5:
        if np.mean([red_channel,
                    green_channel]) >= 140 and np.mean([red_channel, green_channel]) - blue_channel >= 60:
            return True
        else:
            return False
    # Pink
    if color == 6:
        if np.mean([red_channel,
                    blue_channel]) >= 140 and np.mean([red_channel, blue_channel]) - green_channel >= 60:
            return True
        else:
            return False
    # Cyan:
    if color == 7:
        if np.mean([green_channel,
                    blue_channel]) >= 140 and np.mean([green_channel, blue_channel]) - red_channel >= 60:
            return True
        else:
            return False
    # White
    if color == 8:
        if red_channel >= 170 and green_channel >= 170 and blue_channel >= 170:
            avg = np.mean([red_channel, green_channel, blue_channel])
            if red_channel - avg <= 10 and green_channel - avg <= 10 and blue_channel - avg <= 10:
                return True
        else:
            return False


def color_mean(image) -> tuple:
    """

    :param image: input of the image
    :return: return corresponding (R,G,B) values of the cut image
    """
    image_trans = np.transpose(image, (2, 0, 1))
    red_channel = image_trans[0].mean()
    green_channel = image_trans[1].mean()
    blue_channel = image_trans[2].mean()
    print(f"R:{red_channel:.3f} G:{green_channel:.3f} B:{blue_channel:.3f}")
    return red_channel, green_channel, blue_channel


def color_match(img_dir, color_up, color_down) -> bool:
    """

    :param img_dir: the path of the input image
    :param color_up: the colour of upper part of the image that the user provided
    :param color_down: the colour of the down part of the image that the user provided
    :return: whether the image matches the description that the user provided
    """
    # color mapping
    colors_dict = {"黑色": 1, "红色": 2, "绿色": 3, "蓝色": 4, "黄色": 5, "粉色": 6, "青色": 7, "白色": 8}
    color_up = colors_dict[color_up]
    color_down = colors_dict[color_down]
    # input the image
    image = io.imread(img_dir)
    # get the upper part of the image
    up = image.shape[0] * 170 // 1000
    image_up = image[up:up * 3]
    red_up, green_up, blue_up = color_mean(image_up)
    judgment_up = color_judge(red_up, green_up, blue_up, color_up)
    # get the down part of the image
    image_down = image[up * 3:up * 4]
    red_down, green_down, blue_down = color_mean(image_down)
    judgment_down = color_judge(red_down, green_down, blue_down, color_down)
    # plot the concatenate image of the upper and down image
    plt.figure()
    img_cat = np.concatenate((image_up, image_down), axis=0)
    plt.imshow(img_cat)
    plt.plot([0, img_cat.shape[1]], [img_cat.shape[0] * 2 / 3, img_cat.shape[0] * 2 / 3], 'r', 2)
    plt.pause(3)
    plt.close('all')
    # give the final
    if judgment_up is True:
        if judgment_down is True:
            prompt = 'Congratulation! The selected image perfectly matches your description!'
            return prompt
        else:
            prompt = 'Not too bad, The color of the upper body matches your description but not for the lower part ' \
                     'of the body.'
            return prompt
    else:
        if judgment_down is True:
            prompt = 'Not too bad, The color of the lower part of the body matches your description but not for the ' \
                     'upper part '
            return prompt
        else:
            prompt = 'Sorry. The selected image is not the one that you want.'
            return prompt


if __name__ == "__main__":
    print("This is color match program")
    a = color_match('./yellow.png', '黄色', '黄色')
    print(a)
