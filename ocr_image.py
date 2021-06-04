import rotate_image
from collections import namedtuple
import pytesseract
import argparse
import imutils
import cv2

def ocr(image, template) :
    print("[Loading...] OCR Location Setting")

    OCRLocation = namedtuple("OCRLocation", ["id", "bbox", "filter_keywords"])

    OCR_Locations = [
        OCRLocation("name", (27, 96, 60, 20), []),
        OCRLocation("address", (27, 115, 276, 21), []),
        OCRLocation("detail_address", (28, 134, 409, 36), []),
    ]

    print("[Loading...] aligning images")
    aligned = rotate_image.rotate_image(image, template)

    print("[Loading...] Proceeding OCR")
    parsingResults = []

    for loc in OCR_Locations:
        (x, y, w, h) = loc.bbox
        roi = aligned[y:y+h, x:x+w]
        # cv2.imshow(loc.id, roi)
        # cv2.waitKey(0)
    
        rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(rgb, lang='kor')
    
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
        print("{}\n".format(text))

    # cv2.imshow("Input", imutils.resize(image))
    # cv2.imshow("Output", imutils.resize(aligned))
    # cv2.waitKey(0)
    
    return results
