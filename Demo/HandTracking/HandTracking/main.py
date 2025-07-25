import argparse
import os
import time

import cv2
import numpy as np
import pyarrow as pa
from dora import Node
import mediapipe as mp
from scipy.spatial.transform import Rotation

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def process_img(hand_proc, image):
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hand_proc.process(image)

    # Draw the hand annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    res=None
    if results.multi_hand_landmarks:

      # print('Handedness:', results.multi_handedness)
      # print(results.multi_hand_world_landmarks)

      for index,handedness_classif in enumerate(results.multi_handedness):
          if handedness_classif.classification[0].label=='Right' and handedness_classif.classification[0].score>0.8: #let's considere only one right hand


      # for hand_landmarks in results.multi_hand_landmarks:
      #     tip_x=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x-hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
      #     tip_y=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y-hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
      #     tip_z=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z-hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].z
      #     print(f'TIP: {tip_x} {tip_y} {tip_z}')
      #     mp_drawing.draw_landmarks(
      #         image,
      #         hand_landmarks,
      #         mp_hands.HAND_CONNECTIONS,
      #         mp_drawing_styles.get_default_hand_landmarks_style(),
      #         mp_drawing_styles.get_default_hand_connections_style())


              hand_landmarks=results.multi_hand_world_landmarks[index] #metric
              # hand_landmarks=results.multi_hand_landmarks[index] #normalized
              hand_landmarks_norm=results.multi_hand_landmarks[index] #normalized

              #TODO rotate everything in a hand referential

              tip1_x=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x-hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x
              tip1_y=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y-hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
              tip1_z=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z-hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].z

              tip2_x=hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x-hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x
              tip2_y=hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y-hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
              tip2_z=hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].z-hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].z

              tip3_x=hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x-hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].x
              tip3_y=hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y-hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y
              tip3_z=hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].z-hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].z

              tip4_x=hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x-hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].x
              tip4_y=hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y-hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].y
              tip4_z=hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].z-hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_MCP].z


              # tip1_x=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
              # tip1_y=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
              # tip1_z=hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z


              # print(f'TIP: {tip_x} {tip_y} {tip_z} ({hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x} {hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y} {hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].z})')
              mp_drawing.draw_landmarks(
                  image,
                  hand_landmarks_norm,
                  mp_hands.HAND_CONNECTIONS,
                  mp_drawing_styles.get_default_hand_landmarks_style(),
                  mp_drawing_styles.get_default_hand_connections_style())


              #define a new hand frame centered at marker WRIST (n°0) with z along the vector (WRIST,MIDDLE_FINGER_MCP) (0,9) and x is the "third dimension" normal to the plan of the palm (WRIST,MIDDLE_FINGER_MCP)x(WRIST,PINKY_MCP)
              # origin=np.array([hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x,hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y,hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].z])
              # mid_mcp=np.array([hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x,hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y,hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].z])
              # unit_z=mid_mcp-origin
              # unit_z=unit_z/np.linalg.norm(unit_z)
              # pinky_mcp=np.array([hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].x,hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].y,hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_MCP].z])

              origin=np.array([hand_landmarks_norm.landmark[mp_hands.HandLandmark.WRIST].x,hand_landmarks_norm.landmark[mp_hands.HandLandmark.WRIST].y,hand_landmarks_norm.landmark[mp_hands.HandLandmark.WRIST].z])
              mid_mcp=np.array([hand_landmarks_norm.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x,hand_landmarks_norm.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y,hand_landmarks_norm.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].z])
              unit_z=mid_mcp-origin
              unit_z=unit_z/np.linalg.norm(unit_z)
              pinky_mcp=np.array([hand_landmarks_norm.landmark[mp_hands.HandLandmark.PINKY_MCP].x,hand_landmarks_norm.landmark[mp_hands.HandLandmark.PINKY_MCP].y,hand_landmarks_norm.landmark[mp_hands.HandLandmark.PINKY_MCP].z])

              # print(f"ORIGIN: {origin} MID: {mid_mcp}")
              vec_towards_y=pinky_mcp-origin
              # unit_x=np.cross(unit_z,vec_towards_y)
              unit_x=np.cross(vec_towards_y,unit_z)


              unit_x=unit_x/np.linalg.norm(unit_x)
              unit_y=np.cross(unit_z,unit_x)
              # unit_y=np.cross(unit_x,unit_z)

              # A=np.array([unit_x,unit_y,unit_z]).reshape((3,3))
              R=np.array([unit_x,-unit_y,unit_z]).reshape((3,3)) #-y because of mirror?


              # tip1=np.array([tip1_x,tip1_y,tip1_z]).dot(R)
              # tip2=np.array([tip2_x,tip2_y,tip2_z]).dot(R)
              # tip3=np.array([tip3_x,tip3_y,tip3_z]).dot(R)
              # tip4=np.array([tip4_x,tip4_y,tip4_z]).dot(R)

              # tip1=np.array([tip1_x,tip1_y,tip1_z]).dot(R)
              tip1=R@np.array([tip1_x,tip1_y,tip1_z])
              tip2=R@np.array([tip2_x,tip2_y,tip2_z])
              tip3=R@np.array([tip3_x,tip3_y,tip3_z])
              tip4=R@np.array([tip4_x,tip4_y,tip4_z])

              # scale=0.01
              # image = cv2.drawFrameAxes(image, K, disto, rotV, origin, scale)

              # res=[{'r_tip1': [tip1_x,tip1_y,tip1_z],'r_tip2': [tip2_x,tip2_y,tip2_z],'r_tip3': [tip3_x,tip3_y,tip3_z],'r_tip4': [tip4_x,tip4_y,tip4_z]}]
              res=[{'r_tip1': tip1,'r_tip2': tip2,'r_tip3': tip3,'r_tip4': tip4}]
    # Flip the image horizontally for a selfie-view display.
    return image,res
# cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))


def main():

    node = Node()


    pa.array([])  # initialize pyarrow array
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:



        for event in node:

            event_type = event["type"]

            if event_type == "INPUT":
                event_id = event["id"]

                if event_id == "tick":
                    ret, frame = cap.read()

                    if not ret:
                        continue

                    frame = cv2.flip(frame, 1)
                    #process
                    frame,res=process_img(hands,frame)

                    if res is not None:
                        node.send_output('hand_pos',pa.array(res))
                    # cv2.imshow('MediaPipe Hands', cv2.flip(frame, 1))
                    cv2.imshow('MediaPipe Hands', frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break


            elif event_type == "ERROR":
                raise RuntimeError(event["error"])


if __name__ == "__main__":
    main()
