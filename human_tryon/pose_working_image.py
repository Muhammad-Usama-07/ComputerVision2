# ######## dynamic

# import cv2
# from cvzone.PoseModule import PoseDetector
# import cvzone
# import numpy as np

# cap = cv2.VideoCapture("rtsp://192.168.100.177/") 
# detector = PoseDetector()
# shirt_path = '1-removebg-preview.png'
# fixedRatio = 262/190 #widthOfshirt/widthOfpoint_11_12
# shortRatioWidthHeight = 581/440
# def calculate_distance(keypoint1, keypoint2):
#     # Keypoints are assumed to be tuples of (x, y)
#     x1, y1 = keypoint1
#     x2, y2 = keypoint2

#     # Calculate Euclidean distance
#     distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

#     return distance

# while True:
#     success, img = cap.read()
#     img = detector.findPose(img)
#     lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False) 
#     imgShirt = cv2.imread(shirt_path, cv2.IMREAD_UNCHANGED)
#     # cvzone.overlayPNG(img, imgShirt, (100,100))
#     # print(lmList)
#     if lmList:
#         print(lmList)
#         print('\n\n------------- length of points', len(lmList))

#         lm11 = lmList[11][0:2]
#         lm12 = lmList[12][0:2]

#         print('------------- distance between points', calculate_distance(lm11, lm12))
#         imgShirt = cv2.imread(shirt_path, cv2.IMREAD_UNCHANGED)
#         # imgShirt = cv2.resize(imgShirt, (0,0), None, 0.5, 0.5)
        
#         # wsidthOfShirt = int((lm12[0]-lm11[0])*fixedRatio)

#         wsidthOfShirt = max(1, int((lm11[0] - lm12[0]) * fixedRatio))

#         print('------------- width of shirt', wsidthOfShirt,'\n\n')
#         # imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt*shortRatioWidthHeight)))
#         imgShirt = cv2.resize(imgShirt, (wsidthOfShirt, max(1, int(wsidthOfShirt*shortRatioWidthHeight))))
#         currentScale = (lm11[0] - lm12[0]) / 190
#         offset = (int(44 * currentScale), int(48 * currentScale))

#         try:
#             img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
#         except:
#             pass



#         # try:
#         #     img = cvzone.overlayPNG(img, imgShirt, lm12)
#         # except:
#         #     pass




#         # imgShirt = cv2.resize(imgShirt, (0,0), None, 0.5, 0.5)
#         # # cvzone.overlayPNG(img, imgShirt, (100,100))
#         # try:
#         #     cvzone.overlayPNG(img, imgShirt, lm12)
#         # except:
#         #     pass
#         # pass
#         # center = bboxInfo["center"]
#         # lm11 = lmList[11][1:3]
#         # lm12 = lmList[12][1:3]
#         # imgShirt = cv2.imread('1-removebg-preview.png' ,cv2.IMREAD_UNCHANGED)
#         # # imgShirt = cv2.resize(imgShirt, (0,0), None, 0.5, 0,5)
#         # try:
#         #     img = cvzone.overlayPNG(img, imgShirt, lm11)
#         # except:
#         #     pass
        
#         # cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)


###### dynamic size camera working code 

# import cv2
# from cvzone.PoseModule import PoseDetector
# import cvzone
# import numpy as np

# # cap = cv2.VideoCapture("rtsp://192.168.100.177/live/ch00_1") 
# cap = cv2.VideoCapture("http://192.168.100.126:8080/video") 

# detector = PoseDetector()
# shirt_path = 'shirts/1.png'
# fixedRatio = 262/190  # widthOfshirt/widthOfpoint_11_12
# shortRatioWidthHeight = 581/440

# def calculate_distance(keypoint1, keypoint2):
#     x1, y1 = keypoint1
#     x2, y2 = keypoint2
#     distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
#     return distance

# while True:
#     success, img = cap.read()
#     img = detector.findPose(img)
#     lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False) 
#     imgShirt = cv2.imread(shirt_path, cv2.IMREAD_UNCHANGED)
    
#     if lmList:
#         # Print and calculate distance between points
#         print(lmList)
#         print('\n\n------------- length of points', len(lmList))
#         lm11 = lmList[11][0:2]
#         lm12 = lmList[12][0:2]
#         print('------------- distance between points', calculate_distance(lm11, lm12))

#         # Resize shirt
#         wsidthOfShirt = max(1, int((lm11[0] - lm12[0]) * fixedRatio))
#         imgShirt = cv2.resize(imgShirt, (wsidthOfShirt, max(1, int(wsidthOfShirt * shortRatioWidthHeight))))
        
#         # Overlay the shirt on the image
#         currentScale = (lm11[0] - lm12[0]) / 190
#         offset = (int(44 * currentScale), int(48 * currentScale))
#         try:
#             img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
#         except:
#             pass

#     # Draw the image without keypoints
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)

###### Dynamic size image working code

import cv2
from cvzone.PoseModule import PoseDetector
import cvzone
import numpy as np

# Read a single image
img = cv2.imread("person1.jpg")

detector = PoseDetector()
shirt_path = 'shirts/1.png'
fixedRatio = 262/190  # widthOfshirt/widthOfpoint_11_12
shortRatioWidthHeight = 581/440

def calculate_distance(keypoint1, keypoint2):
    x1, y1 = keypoint1
    x2, y2 = keypoint2
    distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance

# Process the image
img = detector.findPose(img)
lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False) 
imgShirt = cv2.imread(shirt_path, cv2.IMREAD_UNCHANGED)

if lmList:
    # Print and calculate distance between points
    print(lmList)
    print('\n\n------------- Total number of points', len(lmList))
    lm11 = lmList[11][0:2]
    lm12 = lmList[12][0:2]
    print('------------- distance between points', calculate_distance(lm11, lm12))
    print('------------- lm11, lm12', lm11, lm12)
    # Resize shirt
    wsidthOfShirt = max(1, int((lm11[0] - lm12[0]) * fixedRatio))
    print('------------- wsidthOfShirt: ', wsidthOfShirt)
    print('------------- shortRatioWidthHeight: ', shortRatioWidthHeight)

    print('------------- max(1, int(wsidthOfShirt * shortRatioWidthHeight): ', max(1, int(wsidthOfShirt * shortRatioWidthHeight)))


    imgShirt = cv2.resize(imgShirt, (wsidthOfShirt, max(1, int(wsidthOfShirt * shortRatioWidthHeight))))
    
    # Overlay the shirt on the image
    currentScale = (lm11[0] - lm12[0]) / 190
    offset = (int(44 * currentScale), int(48 * currentScale))

    print('------------- offset: ', offset)
    print('------------- currentScale: ', currentScale)


    try:
        img = cvzone.overlayPNG(img, imgShirt, (lm12[0] - offset[0], lm12[1] - offset[1]))
    except:
        pass

# Display the image
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
######### fixed accessories

# import cv2
# from cvzone.PoseModule import PoseDetector
# import cvzone
# import numpy as np

# cap = cv2.VideoCapture("rtsp://192.168.100.177/live/ch00_1") 
# detector = PoseDetector()
# shirt_path = 'accessories/scraf.png'
# fixedRatio = 262/190 #widthOfshirt/widthOfpoint_11_12
# shortRatioWidthHeight = 581/440
# def calculate_distance(keypoint1, keypoint2):
#     # Keypoints are assumed to be tuples of (x, y)
#     x1, y1 = keypoint1
#     x2, y2 = keypoint2

#     # Calculate Euclidean distance
#     distance = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

#     return distance

# while True:
#     success, img = cap.read()
#     # (h, w) = img.shape[:2]
#     # print('h and w :    ', (h, w))
#     # img = detector.findPose(img)
#     # lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False) 
#     img = cv2.flip(img, 1)
#     imgShirt = cv2.imread(shirt_path, cv2.IMREAD_UNCHANGED)
#     imgShirt = cv2.resize(imgShirt, (159,170), interpolation = cv2.INTER_AREA)
#     # print(lmList)
#     # print('length of points -------------', len(lmList))

#     # lm11 = lmList[11][0:2]
#     # lm12 = lmList[12][0:2]

#     # print('distance between points', calculate_distance(lm11, lm12))
#     # imgShirt = cv2.imread(shirt_path, cv2.IMREAD_UNCHANGED)
#     # # imgShirt = cv2.resize(imgShirt, (0,0), None, 0.5, 0.5)
    
#     # widthOfShirt = int((lm12[0]-lm11[0])*fixedRatio)
#     # print('width of shirt', widthOfShirt)
#     # imgShirt = cv2.resize(imgShirt, (widthOfShirt, int(widthOfShirt*shortRatioWidthHeight)))
#     #### imgShirt = cv2.resize(imgShirt, (max(1, widthOfShirt), max(1, int(wsidthOfShirt*shortRatioWidthHeight))))


#     try:
#         img = cvzone.overlayPNG(img, imgShirt, (650, 220))
#     except:
#         pass




#         # imgShirt = cv2.resize(imgShirt, (0,0), None, 0.5, 0.5)
#         # # cvzone.overlayPNG(img, imgShirt, (100,100))
#         # try:
#         #     cvzone.overlayPNG(img, imgShirt, lm12)
#         # except:
#         #     pass
#         # pass
#         # center = bboxInfo["center"]
#         # lm11 = lmList[11][1:3]
#         # lm12 = lmList[12][1:3]
#         # imgShirt = cv2.imread('1-removebg-preview.png' ,cv2.IMREAD_UNCHANGED)
#         # # imgShirt = cv2.resize(imgShirt, (0,0), None, 0.5, 0,5)
#         # try:
#         #     img = cvzone.overlayPNG(img, imgShirt, lm11)
#         # except:
#         #     pass
        
#         # cv2.circle(img, center, 5, (255, 0, 255), cv2.FILLED)
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)


# import cv2
# from cvzone.PoseModule import PoseDetector
# import cvzone
# import numpy as np

# detector = PoseDetector()
# shirt_path = '1-removebg-preview.png'
# img = cv2.imread('person1.jpg')
# img = detector.findPose(img)
# lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False, draw=False) 
# imgShirt = cv2.imread(shirt_path, cv2.IMREAD_UNCHANGED)
# try:
#     img = cvzone.overlayPNG(img, imgShirt, (100,100))
# except:
#     pass
# cv2.imshow("Image", img)
# cv2.waitKey(0)