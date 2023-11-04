c = max(contours, key = cv2.contourArea)
M = cv2.moments(c)

cx = int(M['m10']/M['m00'])

if cx<55 or cx > 90:
    motor.left()
elif cx>=39 and cx <=65:
    motor.right()
else:
    motor.go()