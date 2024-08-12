from flask import Flask, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS    # Import CORS from flask_cors
import base64
import numpy as np
import cv2
import json
import cvzone
import ast
import torch
from torchvision import transforms
from ultralytics import YOLO
# import pdb


app = Flask(__name__)
socketio = SocketIO(app)
CORS(app)  # Enable CORS for all routes
# Load the YOLO model
model = YOLO('best.pt')
# Constants
BOX_CONF_THRESH = 0.5
BOX_IOU_THRESH = 0.5
KPT_CONF_THRESH = 0.5
inc = 15
users = {}

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
    return resized_img, new_width, new_height

def wear_cap(cap_img,animal_image,  filter_kpts):
    ############################### cap working ############################### 
    
    print('Shape of animal_image:', animal_image.shape)
    print('Data type of animal_image:', animal_image.dtype)

    ################# Check two points (if 14 and 15 exist in the third item of each list)
    
    # get value of 14 and 15
    point_14 = next(sublist for sublist in filter_kpts if sublist[2] == 14)
    point_15 = next(sublist for sublist in filter_kpts if sublist[2] == 15)
    if point_14 and point_15:
        print("********************* Both 14 and 15 exist.")
        # Calculate the width between points 14 and 15
        width_14_15 = np.sqrt((point_14[0] - point_15[0])**2 + (point_14[1] - point_15[1])**2)
        resized_accessories_img, new_width, new_height  = resize_with_aspect_ratio(cap_img, int(width_14_15))
        print(f"********************* The width between points 14 and 15 is: {width_14_15}")
        print(f"##################### New height and width: {new_width }, {new_height}")
        
        return new_width, new_height, point_15
    else:
        print('unable to detect points')
        return 0,0, point_15



def wear_collar(cap_img,animal_image,  filter_kpts):
    ############################### collar working ############################### 
    
    print('Shape of animal_image:', animal_image.shape)
    print('Data type of animal_image:', animal_image.dtype)

    ################# Check two points (if 14 and 15 exist in the third item of each list)
    
    # get value of 14 and 15
    point_8 = next(sublist for sublist in filter_kpts if sublist[2] == 8)
    point_2 = next(sublist for sublist in filter_kpts if sublist[2] == 2)
    if point_8 and point_2:
        print("********************* Both 14 and 15 exist.")
        #### width between 8 and 2
        width_8_2 = np.sqrt((point_2[0] - point_8[0])**2 + (point_2[1] - point_8[1])**2)
        resized_accessories_img, new_width, new_height  = resize_with_aspect_ratio(cap_img, int(width_8_2))
        print(f"********************* The width between points 14 and 15 is: {width_8_2}")
        print(f"##################### New height and width: {new_width }, {new_height}")
        # Calculate the midpoint
        midpoint_x = int((point_2[0] + point_8[0]) / 2)
        midpoint_y = int((point_2[1] + point_8[1]) / 2)
        point_17 = next(sublist for sublist in filter_kpts if sublist[2] == 17)
        
        mid_17_bet_width_8_2 = np.sqrt((midpoint_x - point_17[0])**2 + (midpoint_y - point_17[1])**2)
        # print('width between mid and 17: ', mid_17_bet_width_8_2)

        if mid_17_bet_width_8_2 <= 100:
            percentage_to_subtract = 35
            offset_y = int(percentage_to_subtract / 100 * resized_accessories_img.shape[1])
            point_to_send = point_8[0] , point_8[1] - offset_y
            image = cvzone.overlayPNG(animal_image, resized_accessories_img, (point_8[0] , point_8[1] - offset_y))
            
        else:
            midpoint_x_17 = int((midpoint_x + point_17[0]) / 2)
            midpoint_y_17 = int((midpoint_y + point_17[1]) / 2)
            # print("^^^^^^^^^^^^^^^^ mid between mid and 7 ", midpoint_x_17, midpoint_y_17)
            
            ######## show point in specific location
            percentage_to_subtract = 45
            offset_y = int(percentage_to_subtract / 100 * resized_accessories_img.shape[1])
            point_to_send = (midpoint_x_17 - offset_y, midpoint_y_17 - offset_y)
            image = cvzone.overlayPNG(animal_image, resized_accessories_img, (midpoint_x_17 - offset_y, midpoint_y_17 - offset_y))
        
        return new_width, new_height, point_to_send
    else:
        print('unable to detect points')
        return 0,0, 0

def base64_to_image_opencv(base64_string):
    try:
        # Decode the Base64 string
        image_data = base64.b64decode(base64_string)
        
        # Convert the decoded image data to a NumPy array
        img_nparr = np.frombuffer(image_data, np.uint8)

        return img_nparr
    except Exception as e:
        print("Error:", str(e))
        return None

@socketio.on("connect")
def handle_connect():
    print("Client connected!")
    socketio.emit("server_message", "connection ka msg")


@socketio.on("new_message")
def handle_new_message(data):
    # print(data)
    # data = {
    #     'eventName'
    #     'ani_img'
    #     'cat_prod_img'
    #     'catag_name'
    #     'dim_update'
    # }
    #convert string to  object
    json_data = json.loads(data)
    # print('====== json_data =====', json_data)
    print('---------- byte received ---------')
    try:
        # Extract Base64 string from data
        # base64_string = data.get("image_data")
        # pdb.set_trace()
        # socketio.emit(json_data['eventName'], "Image processed successfully")
        
        if json_data['ani_img']:
            print('------ image exits in json ------')

            dim_update = ast.literal_eval(json_data['dim_update'])

            # Convert Base64 to image using OpenCV
            ani_img = base64_to_image_opencv(json_data['ani_img'])
            # Decode the NumPy array to an OpenCV image
            ani_img = cv2.imdecode(ani_img, cv2.IMREAD_COLOR)
            # ani_img = cv2.resize(ani_img, dim_update)

            # cv2.imwrite('animal_img.jpg', ani_img) 
            ani_img = cv2.resize(ani_img, (1000, 667))
            ani_img = cv2.rotate(ani_img, cv2.ROTATE_90_CLOCKWISE)

            acc_img = base64_to_image_opencv(json_data['cat_prod_img'])
            # Decode the NumPy array to an OpenCV image

            acc_img = cv2.imdecode(acc_img, cv2.IMREAD_UNCHANGED)
            # cv2.imwrite('catagory_image.jpg', acc_img) 

            if ani_img is not None:
                print('-- animal image recieved')
                print('-- dimension received', json_data['dim_update'])
                # Display the image (optional)
                # cv2.imshow("Image", result_image)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                # emit("message -------------------- gaya")
                # emit("acknowledgment", "Image processed successfully")
                cv2.imwrite('ani_img_before_result.jpg', ani_img)
                
                # Perform YOLO predictions
                results = model.predict(ani_img, conf=BOX_CONF_THRESH, iou=BOX_IOU_THRESH)[0].cpu()
                # print('************** results **************', results)

                cv2.imwrite('ani_img_after_result.jpg', ani_img)
                if results is None or results == []:
                    # return jsonify({'error': 'No predictions please enter correct image'})
                    socketio.emit(json_data['eventName'], "No predictions please enter correct image")

                else:
                    try:
                        # pdb.set_trace()
                        pred_kpts_xy = results.keypoints.xy.numpy()
                        print('\n pred_kpts_xy: ', pred_kpts_xy)
                        pred_kpts_conf = results.keypoints.conf.numpy()
                        
                        print('\n pred_kpts_conf: ', pred_kpts_conf, '\n\n')

                        filter_kpts = []
                        # Draw predicted bounding boxes, conf scores and keypoints on image.
                        for kpts, confs in zip(pred_kpts_xy, pred_kpts_conf):
                            kpts_ids = np.where(confs > KPT_CONF_THRESH)[0]
                            filter_kpts = kpts[kpts_ids]
                            filter_kpts = np.concatenate([filter_kpts, np.expand_dims(kpts_ids, axis=-1)], axis=-1)
                            filter_kpts = [[int(x) for x in inner_list] for inner_list in filter_kpts]
                            print('******* filter_kpts: ', filter_kpts)
                            print('catag_name =====', json_data['catag_name'])
                            if json_data['catag_name'] == "collarbelt":

                                print('collarbelt per aya tha')
                                width, height, point_8 = wear_collar(acc_img, ani_img, filter_kpts) 
                                _, img_encoded = cv2.imencode('.png', cv2.cvtColor(ani_img, cv2.COLOR_RGB2BGR))
                                img_base64 = base64.b64encode(img_encoded).decode('utf-8')
                                print('point_8', point_8, ' ------- width, height', width, height)
                                response_data = {'image': img_base64,'ps':0.0 ,'loc': point_8,  'wid_high':[width, height]}
                        
                            elif json_data['catag_name'] == "cap":
                                print('cap per aya tha')
                                width, height, point_15 = wear_cap(acc_img, ani_img, filter_kpts) 
                                _, img_encoded = cv2.imencode('.png', cv2.cvtColor(ani_img, cv2.COLOR_RGB2BGR))
                                img_base64 = base64.b64encode(img_encoded).decode('utf-8')
                                response_data = {'image': img_base64,'ps':0.7 , 'loc': point_15,  'wid_high':[width, height]}

                            else:
                                print('Please give catagory name')
                                # socketio.emit(json_data['eventName'], 'error: Please give catagory name')
                            socketio.emit(json_data['eventName'], response_data)

                    except:
                        socketio.emit(json_data['eventName'], 'error: transformation error')

                # socketio.emit("server_message", "server:Image processed successfully")
                # socketio.emit(json_data['eventName'], "Image processed successfully")
                # print('---------- result displayed ---------')
        else:
            # emit("message-------------------- gaya")  
            print('data ya aya hy', data)
    except Exception as e:
        # emit("message-------------------- gaya").
        socketio.emit("server_message", "got exception")
        print('Error processing image data:', e)
if __name__ == "__main__":
    socketio.run(app, '0.0.0.0', port=5555, debug=True)
