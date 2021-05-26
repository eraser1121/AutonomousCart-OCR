import align_images
from collections import namedtuple
import pytesseract
import argparse
import imutils
import cv2

def cleanup_text(text):
    return "".join([c if ord(c) < 128 else "" for c in text]).strip()

OCRLocation = namedtuple("OCRLocation", ["id", "bbox", "filter_keywords"])

OCR_Locations = [
    OCRLocation("first_name", (27, 96, 60, 20), []),
    OCRLocation("address", (27, 115, 276, 21), []),
    OCRLocation("detail_address", (28, 134, 409, 36), []),
]

print("[Info] loading images...")
image = cv2.imread("cap_img.jpg")
template = cv2.imread("myform.jpg")

print("[Info] aligning images...")
aligned = align_images.align_images(image, template)

print("[Info] OCR'ing document...")
parsingResults = []

for loc in OCR_Locations:
    (x, y, w, h) = loc.bbox
    roi = aligned[y:y+h, x:x+w]
    cv2.imshow(loc.id, roi)
    cv2.waitKey(0)
    
    rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb, lang='Hangul')
    
    for line in text.split("\n"):
        if len(line) == 0:
            continue

        lower = line.lower()
        count = sum([lower.count(x) for x in loc.filter_keywords])

        if count == 0:
            parsingResults.append((loc, line))

results = {}

for (loc, line) in parsingResults:
    r = results.get(loc.id, None)

    if r is None:
        results[loc.id] = (line, loc._asdict())
    
    else:
        (existingText, loc) = r
        text = "{}\n{}".format(existingText, line)

        results[loc["id"]] = (text, loc)

for (locID, result) in results.items():
    (text, loc) = result

    print(loc["id"])
    print("=" * len(loc["id"]))
    print("{}\n\n".format(text))

    (x, y, w, h) = loc["bbox"]
    clean = cleanup_text(text)

    cv2.rectangle(aligned, (x, y), (x+w, y+h), (0, 255, 0), 2)

    for (i, line) in enumerate(clean.split("\n")):
        startY = y + (i * 70) + 40
        cv2.putText(aligned, line, (x, startY), cv2.FONT_HERSHEY_SIMPLEX, 1.8, (0, 0, 255), 5)

cv2.imshow("Input", imutils.resize(image))
cv2.imshow("Output", imutils.resize(aligned))
cv2.waitKey(0)
