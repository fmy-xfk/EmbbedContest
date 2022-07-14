import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.75, min_tracking_confidence=0.5)
mpDraw = mp.solutions.drawing_utils 

def process_frame(img):
    start_time = time.time()
    h, w = img.shape[0], img.shape[1]
    img=cv2.flip(img, 1)
    results = hands.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks: # 如果有检测到手
        handness_str = ''
        index_finger_tip_str = ''
        for hand_idx in range(len(results.multi_hand_landmarks)):
            hand_21 = results.multi_hand_landmarks[hand_idx]
            mpDraw.draw_landmarks(img, hand_21, mp_hands.HAND_CONNECTIONS)
            temp_handness = results.multi_handedness[hand_idx].classification[0].label
            handness_str += '{}:{} '.format(hand_idx, temp_handness)

            # 获取手腕根部深度坐标
            cz0 = hand_21.landmark[0].z

            for i in range(21): # 遍历该手的21个关键点

                # 获取3D坐标
                cx = int(hand_21.landmark[i].x * w)
                cy = int(hand_21.landmark[i].y * h)
                cz = hand_21.landmark[i].z
                depth_z = cz0 - cz

                # 用圆的半径反映深度大小
                radius = max(int(6 * (1 + depth_z*5)), 0)

                if i == 0: # 手腕
                    img = cv2.circle(img,(cx,cy), radius, (0,0,255), -1)
                if i == 8: # 食指指尖
                    img = cv2.circle(img,(cx,cy), radius, (193,182,255), -1)
                    # 将相对于手腕的深度距离显示在画面中
                    index_finger_tip_str += '{}:{:.2f} '.format(hand_idx, depth_z)
                if i in [1,5,9,13,17]: # 指根
                    img = cv2.circle(img,(cx,cy), radius, (16,144,247), -1)
                if i in [2,6,10,14,18]: # 第一指节
                    img = cv2.circle(img,(cx,cy), radius, (1,240,255), -1)
                if i in [3,7,11,15,19]: # 第二指节
                    img = cv2.circle(img,(cx,cy), radius, (140,47,240), -1)
                if i in [4,12,16,20]: # 指尖（除食指指尖）
                    img = cv2.circle(img,(cx,cy), radius, (223,155,60), -1)

        scaler = 1
        img = cv2.putText(img, handness_str, (25 * scaler, 100 * scaler), cv2.FONT_HERSHEY_SIMPLEX, 1.25 * scaler, (255, 0, 255), 2 * scaler)
        img = cv2.putText(img, index_finger_tip_str, (25 * scaler, 150 * scaler), cv2.FONT_HERSHEY_SIMPLEX, 1.25 * scaler, (255, 0, 255), 2 * scaler)
        
        end_time = time.time()
        FPS = 1/(end_time - start_time)
        img = cv2.putText(img, 'FPS  '+str(int(FPS)), (25 * scaler, 50 * scaler), cv2.FONT_HERSHEY_SIMPLEX, 1.25 * scaler, (255, 0, 255), 2 * scaler)
    return img