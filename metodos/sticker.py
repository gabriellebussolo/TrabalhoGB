
import cv2 as cv
import os
import numpy as np 

# Path to the stickers directory
STICKERS_DIR = 'stickers/'  # Ensure this path is correct
STICKER_MAX_SIZE = 200  # Define the maximum size for the larger dimension of the stickers

# Function to load and resize stickers while maintaining the aspect ratio
def load_stickers():
    stickers = []
    for filename in os.listdir(STICKERS_DIR):
        if filename.endswith(".png"):
            sticker_path = os.path.join(STICKERS_DIR, filename)
            sticker = cv.imread(sticker_path, cv.IMREAD_UNCHANGED)
            if sticker is not None:
                # Calculate the scaling factor to maintain the aspect ratio
                h, w = sticker.shape[:2]
                scaling_factor = STICKER_MAX_SIZE / max(h, w)
                new_size = (int(w * scaling_factor), int(h * scaling_factor))
                sticker = cv.resize(sticker, new_size, interpolation=cv.INTER_AREA)
                stickers.append((filename, sticker))
    return stickers

# Function to overlay stickers on the image
def overlay(background, foreground, x_offset=None, y_offset=None):
    

    bg_h, bg_w, bg_channels = background.shape
    fg_h, fg_w, fg_channels = foreground.shape

    assert bg_channels == 3, f'background image should have exactly 3 channels (RGB). found:{bg_channels}'
    assert fg_channels == 4, f'foreground image should have exactly 4 channels (RGBA). found:{fg_channels}'

    # Center the sticker by default
    if x_offset is None: x_offset = (bg_w - fg_w) // 2
    if y_offset is None: y_offset = (bg_h - fg_h) // 2

    # Ensure x_offset and y_offset are within the bounds of the background image
    x_start = max(0, x_offset)
    y_start = max(0, y_offset)
    x_end = min(bg_w, x_offset + fg_w)
    y_end = min(bg_h, y_offset + fg_h)

    # Calculate the region of interest for the foreground and background images
    fg_roi = foreground[y_start - y_offset:y_end - y_offset, x_start - x_offset:x_end - x_offset]
    bg_roi = background[y_start:y_end, x_start:x_end]

    # Separate alpha and color channels from the foreground image
    foreground_colors = fg_roi[:, :, :3]
    alpha_channel = fg_roi[:, :, 3] / 255  # 0-255 => 0.0-1.0

    # Construct an alpha_mask that matches the image shape
    alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))

    # Combine the background with the overlay image weighted by alpha
    composite = bg_roi * (1 - alpha_mask) + foreground_colors * alpha_mask

    # Overwrite the section of the background image that has been updated
    background[y_start:y_end, x_start:x_end] = composite
    return background

def mouse_click(event, x, y, flags, param):
    img = param.get('img', None)
    sticker = param.get('sticker', None)

    if event == cv.EVENT_LBUTTONDOWN and img is not None and sticker is not None:
        img = overlay(img, sticker, x, y)
        cv.imshow('image', img)
