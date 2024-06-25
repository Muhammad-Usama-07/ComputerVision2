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
inc = 15

def resize_with_aspect_ratio(img, new_width=None, new_height=None):
    # Get the current height and width
    height, width = img.shape[:2]

    # If only width is specified
    if new_width is not None and new_height is None:
        # Calculate the aspect ratio and new height
        aspect_ratio = width / height
        new_height = int(new_width / aspect_ratio)

    # If only height is specified
    elif new_height is not None and new_width is None:
        # Calculate the aspect ratio and new width
        aspect_ratio = height / width
        new_width = int(new_height / aspect_ratio)

    # If both width and height are specified, ignore aspect ratio
    elif new_width is not None and new_height is not None:
        pass

    # Resize the image
    resized_img = cv2.resize(img, (new_width, new_height))
    # resized_img =     cv2.cvtColor(resized_img, cv2.COLOR_BGR2RGB)
    return resized_img
def wear_collar(accessories_img ,animal_image,  filter_kpts):
    ############################### collar working ############################### 
    # get value of 8 and 2
    point_8 = next(sublist for sublist in filter_kpts if sublist[2] == 8)
    point_2 = next(sublist for sublist in filter_kpts if sublist[2] == 2)
    # print('point_8 and point_2', point_8, point_2 )

    ### check if point 8 and point 2 exits 
    if point_8 and point_2:
        # print('exits+++++++++++++++++')

        #### width between 8 and 2
        width_8_2 = np.sqrt((point_2[0] - point_8[0])**2 + (point_2[1] - point_8[1])**2)

        #### resize image according to width if the 8 and 2 points 
        resized_accessories_img  = resize_with_aspect_ratio(accessories_img, int(width_8_2))

        # Calculate the midpoint
        midpoint_x = int((point_2[0] + point_8[0]) / 2)
        midpoint_y = int((point_2[1] + point_8[1]) / 2)
        # print("&&&&&&&& mid between 8 and 2 midpoint_x  and midpoint_y", midpoint_x, midpoint_y)

        
        point_17 = next(sublist for sublist in filter_kpts if sublist[2] == 17)
        
        mid_17_bet_width_8_2 = np.sqrt((midpoint_x - point_17[0])**2 + (midpoint_y - point_17[1])**2)
        # print('width between mid and 17: ', mid_17_bet_width_8_2)

        if mid_17_bet_width_8_2 <= 100:
            percentage_to_subtract = 35
            offset_y = int(percentage_to_subtract / 100 * resized_accessories_img.shape[1])
            image = cvzone.overlayPNG(animal_image, resized_accessories_img, (point_8[0] , point_8[1] - offset_y))
            
        else:
            midpoint_x_17 = int((midpoint_x + point_17[0]) / 2)
            midpoint_y_17 = int((midpoint_y + point_17[1]) / 2)
            # print("^^^^^^^^^^^^^^^^ mid between mid and 7 ", midpoint_x_17, midpoint_y_17)
            
            ######## show point in specific location
            percentage_to_subtract = 45
            offset_y = int(percentage_to_subtract / 100 * resized_accessories_img.shape[1])
            
            image = cvzone.overlayPNG(animal_image, resized_accessories_img, (midpoint_x_17 - offset_y, midpoint_y_17 - offset_y))
        
        return image, 'image transforms successfully'
        
        
    else:
        missing_points = [point for point in points_to_check if point not in [sublist[2] for sublist in filter_kpts]]
        print(f" ************The following points are missing: {missing_points}")

        return animal_image, 'points not detected'
    ############################## collar working end ###############################

# Read the image with alpha channel (unchanged)
acc_img = cv2.imread('เต้าหู้-1165.png', cv2.IMREAD_UNCHANGED)

# Open a connection to the webcam (0 is usually the default camera)
cap = cv2.VideoCapture('http://192.168.100.81:8080/video')

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, ani_img = cap.read()

    if not ret:
        print("Error: Failed to capture image.")
        break
    # Resize the frame to a smaller size
    width = 640  # Set desired width
    height = 450  # Set desired height
    ani_img = cv2.resize(ani_img, (width, height))

    results = model.predict(ani_img, conf=BOX_CONF_THRESH, iou=BOX_IOU_THRESH)[0].cpu()
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

                res_img, response = wear_collar(acc_img, ani_img, filter_kpts)
                print('Shape of res_img:', res_img.shape)
                print('Data type of res_img:', res_img.dtype)
                print('Content of res_img:', res_img)
                
                cv2.imshow('Webcam Frame', res_img)
        except Exception as e:
            print('---------------- prediction error ', e)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
