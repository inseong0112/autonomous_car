import cv2

def main():
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)
    camera.set(4, 480)

    while(camera.isOpened()):
        ret, frame = camera.read()
        cv2.imshow('frame', frame)
        # ROI 지정
        crop_img = frame[320:480, 0:640]

        # 흑백 변환
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        # Gaussian Blur 적용
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        median = cv2.medianBlur(blur, 3, 0)
        # 이진화 (흰색 강조)
        _, thresh = cv2.threshold(blur, 160, 255, cv2.THRESH_BINARY_INV)

        #수축, 팽창으로 노이즈 제거 
        mask = cv2.erode(thresh, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        canny_mask = cv2.Canny(mask, 50, 150)
        cv2.imshow('mask', mask)
        cv2.imshow('canny_mask', canny_mask)


        canny_median = cv2.Canny(median, 50, 150)
        
        cv2.imshow('median', median)
        cv2.imshow('canny_median', canny_median)
        if cv2.waitKey(1) == ord('q') :
            break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()


