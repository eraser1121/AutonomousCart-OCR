import cv2
import numpy as np
import ocr_form

image = cv2.imread("myimg1.png")
template = cv2.imread("myform.jpg")

ocr_result = ocr_form.ocr(image, template)

(name, result) = ocr_result["name"]
(address, result) = ocr_result["address"]
(detail_address, result) = ocr_result["detail_address"]

name = name.replace(" ","")
address = address.replace(" ","")
detail_address = detail_address.replace(" ","")

print(name)
print(address)
print(detail_address)
