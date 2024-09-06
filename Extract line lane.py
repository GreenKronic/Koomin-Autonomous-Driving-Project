# line lane 추출 코드 
import cv2
import numpy as np

IMG_WIDTH = 640  # 가로 픽셀값
IMG_HEIGHT = 480  # 세로 픽셀값
PERSPECTIVE_IMG_W = 640
PERSPECTIVE_IMG_H = 480

Source = np.float32([[0, 0], [-300, 340], [640, 0], [940, 340]])
Destination = np.float32([[0, 0], [0, PERSPECTIVE_IMG_H], [PERSPECTIVE_IMG_W, 0], [PERSPECTIVE_IMG_W, PERSPECTIVE_IMG_H]])

def perspective_transform(img):
    # Source의 좌표들을 Destination의 좌표들로 변환하는 변환 행렬(Matrix)을 계산해낸 뒤,
    matrix = cv2.getPerspectiveTransform(Source, Destination)
    # warpPerspective함수를 사용하여 변환 행렬 값을 적용한 result_img를 구해낸다
    result_img = cv2.warpPerspective(img, matrix, (PERSPECTIVE_IMG_W, PERSPECTIVE_IMG_H))
    return result_img

def canny_edge_detection(img):
    # 3x3 커널을 사용하여 이미지의 노이즈 감소
    mat_blur_img = cv2.blur(img, (3, 3))
    # Canny 이미지로 변환
    mat_canny_img = cv2.Canny(mat_blur_img, 70, 170, 3)
    return mat_canny_img

def main():
    img_width = IMG_WIDTH
    img_height = IMG_HEIGHT

    GREEN = (0, 255, 0)
    RED = (0, 0, 255)
    BLUE = (255, 0, 0)
    YELLOW = (0, 255, 255)

    mat_image_org_color = cv2.imread("/home/pi/Downloads/line_2_0.jpg")

    if mat_image_org_color is None:
        print("빈 영상입니다.")
        return -1

    img_width = mat_image_org_color.shape[1]
    img_height = mat_image_org_color.shape[0]

    cv2.namedWindow("Display window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Display window", img_width, img_height)
    cv2.moveWindow("Display window", 10, 20)

    cv2.namedWindow("Gray Image window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Gray Image window", img_width, img_height)
    cv2.moveWindow("Gray Image window", 700, 20)

    cv2.namedWindow("Canny Edge Image window", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Canny Edge Image window", img_width, img_height)
    cv2.moveWindow("Canny Edge Image window", 10, 500)

    while True:
        mat_image_org_color = cv2.imread("/home/pi/Downloads/line_2_0.jpg")
        mat_image_org_gray = cv2.cvtColor(mat_image_org_color, cv2.COLOR_RGB2GRAY)  # color to gray conversion
        mat_image_canny_edge = canny_edge_detection(mat_image_org_gray)
        
        # Canny Edge 이미지에 Perspective Transform을 적용
        image = perspective_transform(mat_image_canny_edge)
        
        linesP = cv2.HoughLinesP(image, 1, np.pi/180, 50, minLineLength=20, maxLineGap=50)
        print(f"Line Number : {len(linesP)}")
        for line in linesP:
            x1, y1, x2, y2 = line[0]
            # 추출한 Hough line들을 mat_image_org_color IMAGE에 그린다
            cv2.line(mat_image_org_color, (x1, y1), (x2, y2), (0, 0, 255), 3, cv2.LINE_AA)
            print(f"L :[{x1},{y1}] , [{x2},{y2}]")

        print("\n\n\n")

        if mat_image_org_color is None:
            print("빈 영상입니다.")
            break

        cv2.imshow("Display window", mat_image_org_color)
        cv2.imshow("Gray Image window", mat_image_org_gray)
        cv2.imshow("Canny Edge Image window", mat_image_canny_edge)

        if cv2.waitKey(10) > 0:
            break

    cv2.destroyAllWindows()
    return 0

if __name__ == "__main__":
    main()
