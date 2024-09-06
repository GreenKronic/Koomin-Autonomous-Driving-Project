# 카메라를 사용하는 기본 예제

import cv2

IMG_WIDTH = 640  # 가로 픽셀값
IMG_HEIGHT = 480  # 세로 픽셀값

def main():
    img_width = IMG_WIDTH
    img_height = IMG_HEIGHT
    
    # dev/video0 카메라에 접근하여 실행
    cap = cv2.VideoCapture(0)
    
    # 해당 디렉토리에 저장되어 있는 영상을 읽어들여, window를 표시함
    # cap = cv2.VideoCapture("/home/pi/AutoCar/C++/OpenCV/2/images/track-s.mkv")
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, img_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, img_height)

    if not cap.isOpened():
        print("에러 - 카메라를 열 수 없습니다.")
        return -1
    
    # window를 표시
    cv2.namedWindow("Display window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Display window", img_width, img_height)
    cv2.moveWindow("Display window", 10, 10)
    
    while True:
        if not cap.isOpened():
            print("에러 - 카메라를 열 수 없습니다.")
            return -1
        
        ret, mat_image_org_color = cap.read()
        if not ret:
            print("에러 - 프레임을 읽을 수 없습니다.")
            break
        
        cv2.imshow("Display window", mat_image_org_color)
        if cv2.waitKey(5) > 0:
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main()
