import cv2
import numpy as np

chiffres = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 0, 1): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
    (1, 1, 1, 1, 0, 1, 1): 9,
	(1, 0, 1, 1, 1, 1, 1): '',
    (0, 0, 1, 0, 0, 0, 0): '',
    (0, 1, 1, 1, 1, 1, 0): '',
    (0, 0, 0, 1, 1, 1, 1): '',
    (1, 0, 0, 1, 1, 1, 1): '',
    (1, 1, 1, 1, 0, 1, 0): ''
}


def reconnaissance_chiffre(image, chiffres):
    (h, w) = image.shape
    (dh, dw) = (int(h * 0.15), int(w * 0.25))

    segments = [
        ((0, 0), (w, dh)),  # segment 0
        ((0, 0), (dw, h // 2)),  # segment 1
        ((w - dw, 0), (w, h // 2)),  # segment 2
        ((0, (h // 2) - dh // 2), (w, (h // 2) + dh // 2)),  # segment 3
        ((0, h // 2), (dw, h)),  # segment 4
        ((w - dw, h // 2), (w, h)),  # segment 5
        ((0, h - dh), (w, h))  # segment 6
    ]

    segON = np.zeros(7)
    j = 0
    for ((xa, ya), (xb, yb)) in segments:
        segment = image[ya:yb, xa:xb]
        surface = (xb - xa) * (yb - ya)
        somme = cv2.countNonZero(segment)
        try:
            if somme / surface >= 0.5:
                segON[j] = 1
            j += 1
        except ZeroDivisionError as er:
            print("")
    return chiffres[tuple(segON)]



image =cv2.imread("compteur.jpg")
#image = cv2.imread("deux.png")

image_rouge = cv2.inRange(image, (0, 0, 150), (50, 50, 255))
blur = cv2.GaussianBlur(image_rouge, (5, 5), 0)

cv2.imshow('image', image)
cv2.imshow('imageBlur', blur)
cv2.waitKey(0)

cv2.destroyAllWindows()
contours, hierarchy = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)
# print(contours)

digit=[]
moy_w=[]
for i in contours:
    x,y,w,h = cv2.boundingRect(i)
    if w >= 20 and w <= 80 and h >= 100 and h <= 120:
        moy_w.append(w)
    moy_w.append(w)
    key = y * 10 + x
    digit.append((i, key))
    (digits, key) = zip(*sorted(digit, key = lambda b: b[1], reverse=False))
moy_w2=int(np.mean(moy_w))
info = []
for i in digits:
    x,y,w,h = cv2.boundingRect(i)
    if w <= moy_w2 : #cas 1
        x = x + w- moy_w2
        w = moy_w2
    crop = blur[y:y+h ,x:x+w]
    val = reconnaissance_chiffre(crop , chiffres)
    info.append(val)
    print(val)

print(info)

