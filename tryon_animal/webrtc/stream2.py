import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, WebRtcMode
import av
import cv2
from ultralytics import YOLO
import numpy as np
import cvzone

# Load the YOLO model
model = YOLO('best.pt')

# Constants
BOX_CONF_THRESH = 0.5
BOX_IOU_THRESH = 0.5
KPT_CONF_THRESH = 0.5

def wear_cap(cap_img, animal_image, filter_kpts):
    points_to_check = [14, 15, 19, 18]
    all_points_exist = all(point in [sublist[2] for sublist in filter_kpts] for point in points_to_check)
    print(f'----------****** four points exist ******----------{all_points_exist}')

    if all_points_exist:
        print("************ All points exist.")
        
        point_19 = next(sublist for sublist in filter_kpts if sublist[2] == 19)
        point_15 = next(sublist for sublist in filter_kpts if sublist[2] == 15)
        point_18 = next(sublist for sublist in filter_kpts if sublist[2] == 18)
        point_14 = next(sublist for sublist in filter_kpts if sublist[2] == 14)

        if point_19[1] > point_15[1]:
            width_19_15 = np.sqrt((point_19[0] - point_15[0])**2 + (point_19[1] - point_15[1])**2)
            width_18_14 = np.sqrt((point_18[0] - point_14[0])**2 + (point_18[1] - point_14[1])**2)
            point_19[1] = int(point_19[1] - 2 * width_19_15)
            point_18[1] = int(point_18[1] - 2 * width_18_14)
            filter_kpts[-1] = point_19 
            filter_kpts[-2] = point_18
            
        cap = cap_img
        cap_h, cap_w = cap.shape[:2]
        head_coordinates = [item for item in filter_kpts if item[2] in points_to_check]
        head_coordinates_position = sorted(head_coordinates, key=lambda x: x[2], reverse=True)
        head_coordinates_position = [[item[0], item[1]] for item in head_coordinates_position]
        
        pts1 = np.float32([[0, 0], [cap_w, 0], [0, cap_h], [cap_w, cap_h]])
        pts2 = np.float32(head_coordinates_position)
        
        h, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)
        height, width, channels = animal_image.shape
        im1Reg = cv2.warpPerspective(cap_img, h, (width, height))
        
        animal_image_result = cvzone.overlayPNG(animal_image, im1Reg, (0, 0))
        return animal_image_result, 'image transforms successfully'

    elif point_14_exists and point_15_exists:
        point_14 = next(sublist for sublist in filter_kpts if sublist[2] == 14)
        point_15 = next(sublist for sublist in filter_kpts if sublist[2] == 15)
        width_14_15 = np.sqrt((point_14[0] - point_15[0])**2 + (point_14[1] - point_15[1])**2)
        resized_accessories_img  = resize_with_aspect_ratio(cap_img, int(width_14_15))
        percentage_to_subtract = 38 
        offset_y = int(percentage_to_subtract / 100 * resized_accessories_img.shape[1])
        animal_image_result = cvzone.overlayPNG(animal_image, resized_accessories_img, (point_15[0], point_15[1] - offset_y))
        return animal_image_result,  'image transforms successfully'
    
    else:
        missing_points = [point for point in points_to_check if point not in [sublist[2] for sublist in filter_kpts]]
        print(f" ************The following points are missing: {missing_points}")
        return animal_image, 'points not detected'
    ############################### cap working end ###############################

# Read the image with alpha channel (unchanged)
acc_img = cv2.imread('inputs/hat_cap/hat_2.png', cv2.IMREAD_UNCHANGED)

class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")

        # Resize the frame to a smaller size
        width = 640  # Set desired width
        height = 450  # Set desired height
        img = cv2.resize(img, (width, height))

        results = model.predict(img, conf=BOX_CONF_THRESH, iou=BOX_IOU_THRESH)[0].cpu()
        print("*** model's prediction done")

        if results is None or results == []:
            print('+++ result length: ', len(results))
            print('No predictions please enter correct image')
        else:
            try:
                print('+++ result length: ', len(results))
                pred_kpts_xy = results.keypoints.xy.numpy()
                pred_kpts_conf = results.keypoints.conf.numpy()
                print('\n pred_kpts_xy: ', pred_kpts_xy)
                print('\n pred_kpts_conf: ', pred_kpts_conf, '\n\n')

                filter_kpts = []
                for kpts, confs in zip(pred_kpts_xy, pred_kpts_conf):
                    kpts_ids = np.where(confs > KPT_CONF_THRESH)[0]
                    filter_kpts = kpts[kpts_ids]
                    filter_kpts = np.concatenate([filter_kpts, np.expand_dims(kpts_ids, axis=-1)], axis=-1)
                    filter_kpts = [[int(x) for x in inner_list] for inner_list in filter_kpts]

                    res_img, response = wear_cap(acc_img, img, filter_kpts)
                    print('Shape of res_img:', res_img.shape)
                    print('Data type of res_img:', res_img.dtype)
                    print('Content of res_img:', res_img)

                    return av.VideoFrame.from_ndarray(res_img, format="bgr24")
            except Exception as e:
                print('---------------- prediction error ', e)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

st.title("Webcam Stream with Streamlit")

webrtc_streamer(key="example", video_processor_factory=VideoProcessor, mode=WebRtcMode.SENDRECV)
