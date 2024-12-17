### 検出したマーカーのIDをリストで返す
import cv2
from cv2 import aruco
import numpy as np
import time

class MarkSearch :

    ### --- aruco設定 --- ###
    dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()

    def __init__(self, cameraID):
        self.cap = cv2.VideoCapture(cameraID)

    def get_markID(self):
        """
        静止画を取得し、arucoマークのidリストを取得する
        """
        ret, frame = self.cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, dict_aruco, parameters=parameters)

        list_ids = np.ravel(ids)

        return list_ids

 
if __name__ == "__main__" :
    import cv2
    from cv2 import aruco
    import numpy as np
    import time

    ### --- aruco設定 --- ###
    dict_aruco = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters()

    ### --- parameter --- ###
    cameraID = 0
    cam0_mark_search = MarkSearch(cameraID)

    cap = cv2.VideoCapture(cameraID)
    cv2.namedWindow("result")


    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                continue
            cv2.imshow("result",frame)#画像を表示する
            if cv2.waitKey(10) & 0xFF == ord("q"):
                break
            print(' ----- get_markID ----- ')
            print(cam0_mark_search.get_markID())
            time.sleep(0.5)
    except KeyboardInterrupt:
        cam0_mark_search.cap.release()

cv2.destroyAllWindows()#ウィンドウを閉じる
