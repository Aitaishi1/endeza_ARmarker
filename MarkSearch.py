# 必要モジュールのインポート
import cv2
from cv2 import aruco
import numpy as np
import time
import math

constant = 720 * 5.15

# マーカー種類を定義
dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
parameters = aruco.DetectorParameters()
markID = 1 #ここで使用するマーカの種類を指定

# ArucoDetectorオブジェクトを作成
detector = aruco.ArucoDetector(dictionary, parameters)

# Webカメラをキャプチャ
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280) #カメラの横幅の設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720) #カメラの縦幅の設定
cap.set(cv2.CAP_PROP_FPS, 30) #フレームレート

#ラズパイの時にこれは実行するようにする
#cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc("Y","U","Y","V"))

#カメラが開かれなかったときの処理
if not cap.isOpened():
    print("Webカメラが見つかりません")
    exit()

while True:
    # フレームを取得
    ret, frame = cap.read()
    if not ret:
        break

    # グレースケールに変換
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # マーカーを検出
    corners, ids, rejectedCandidates = detector.detectMarkers(gray)

    if markID in np.ravel(ids) :
        index = np.where(ids == markID)[0][0] #num_id が格納されているindexを抽出
        cornerUL = corners[index][0][0]
        cornerUR = corners[index][0][1]
        cornerBR = corners[index][0][2]
        cornerBL = corners[index][0][3]
        center = [(cornerUL[0] + cornerBR[0]) * 0.5, (cornerUL[1] + cornerBR[1]) * 0.5]

        '''
        print('左上 : {}'.format(cornerUL))
        print('右上 : {}'.format(cornerUR))
        print('右下 : {}'.format(cornerBR))
        print('左下 : {}'.format(cornerBL))
        print('中心 : {}'.format(center))
        '''
        #カメラからの距離を求める。distanceが距離でcenterがマーカーの中心の座標
        sidex = (cornerUL[0] - cornerUR[0])
        sidey = (cornerUL[1] - cornerUR[1])
        vertx = (cornerUL[0] - cornerBL[0])
        verty = (cornerUL[1] - cornerBL[1])
        side = math.sqrt(sidex*sidex + sidey*sidey)
        vert = math.sqrt(vertx*vertx + verty*verty)
        
        if side > vert:
            distance = constant / side
            #print("距離は",distance)
        else:
            distance = constant / vert
            #print("距離は",distance)
        
        #time.sleep(0.5) #処理を少なくしたいときに随時使用する

        #print(corners[index])### num_id のマーカーが検出された場合 ###
            #centerが中心の座標

    # 検出したマーカーを描画
    if ids is not None:
        frame = aruco.drawDetectedMarkers(frame, corners, ids)
        #print(f"検出されたマーカーID: {ids.flatten()}")

    # フレームを表示
    cv2.imshow('frame', frame)

    # 'q'キーで終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# リソースを解放
cap.release()
cv2.destroyAllWindows()
