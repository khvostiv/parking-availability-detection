import cv2
import pickle

width, height = 70, 34
display_width, display_height = 438, 520

# Load parking positions from file
try:
    with open('backend/CarParkPos', 'rb') as f:
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

    with open('backend/CarParkPos', 'wb') as f:
        pickle.dump(posList, f)

# Main loop
while True:
    img = cv2.imread('./frontend/assets/media/park_image.png')
    if img is None:
        print("Error: Could not load the image. Check the file path.")
        break

    # Resize the image to display size
    img = cv2.resize(img, (display_width, display_height), interpolation=cv2.INTER_AREA)

    # Draw rectangles
    for pos in posList:
        scaled_pos = (int(pos[0] * display_width / img.shape[1]), int(pos[1] * display_height / img.shape[0]))
        cv2.rectangle(img, scaled_pos, 
                      (scaled_pos[0] + int(width * display_width / img.shape[1]), 
                       scaled_pos[1] + int(height * display_height / img.shape[0])), 
                      (255, 0, 255), 2)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)

    # Exit the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
