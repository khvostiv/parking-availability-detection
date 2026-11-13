from pathlib import Path

import cv2
import pickle

BACKEND_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BACKEND_DIR / "data"
IMAGE_PATH = DATA_DIR / "media" / "park_image.png"
POSITIONS_PATH = DATA_DIR / "CarParkPos.pkl"

width, height = 70, 34
display_width, display_height = 438, 520

try:
    with open(POSITIONS_PATH, "rb") as f:
        posList = pickle.load(f)
except FileNotFoundError:
    print("CarParkPos file not found. Starting with an empty position list.")
    posList = []


def mouseClick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    POSITIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(POSITIONS_PATH, "wb") as f:
        pickle.dump(posList, f)


def main():
    while True:
        img = cv2.imread(str(IMAGE_PATH))
        if img is None:
            print(f"Error: Could not load the image at {IMAGE_PATH}")
            break

        img = cv2.resize(img, (display_width, display_height), interpolation=cv2.INTER_AREA)

        for pos in posList:
            scaled_pos = (
                int(pos[0] * display_width / img.shape[1]),
                int(pos[1] * display_height / img.shape[0]),
            )
            cv2.rectangle(
                img,
                scaled_pos,
                (
                    scaled_pos[0] + int(width * display_width / img.shape[1]),
                    scaled_pos[1] + int(height * display_height / img.shape[0]),
                ),
                (255, 0, 255),
                2,
            )

        cv2.imshow("Image", img)
        cv2.setMouseCallback("Image", mouseClick)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
