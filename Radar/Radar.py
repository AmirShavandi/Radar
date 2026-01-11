import cv2
import numpy as np
import time
import platform
import subprocess

# ===== SETTINGS =====
BEEP_INTERVAL = 1.2   # seconds between siren triggers (extra safety, but we also gate by "only once")

# ===== CASCADE LOADER (face detection) =====
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# ===== GLOBAL =====
last_beep_time = 0
system = platform.system()
alert_spoken = False   # <-- so we only alert once per continuous detection


def play_siren():
    """
    Wee-woo style siren / voice alert.
    - Windows: alternating beeps
    - macOS: 'say' command
    - Other: console bell (fallback)
    """
    global last_beep_time
    now = time.time()
    if now - last_beep_time < BEEP_INTERVAL:
        return
    last_beep_time = now

    try:
        if system == "Windows":
            import winsound
            # quick wee-woo pattern
            for _ in range(2):
                winsound.Beep(900, 250)  # high
                winsound.Beep(600, 250)  # low

        elif system == "Darwin":  # macOS
            # say it once
            subprocess.Popen(["say", "Alert, unidentified object"])

        else:  # Linux / other
            # fallback: just a terminal bell
            print("\a", end="")

    except Exception:
        # if audio fails, just ignore
        pass


# ===== RADAR VIEW =====
def create_radar_base():
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    center = (200, 200)
    color = (0, 255, 0)

    # concentric rings
    for i in range(1, 5):
        cv2.circle(img, center, i * 40, color, 1)

    # faint grid lines
    for x in range(0, 401, 40):
        cv2.line(img, (x, 0), (x, 400), (0, 60, 0), 1)
    for y in range(0, 401, 40):
        cv2.line(img, (0, y), (400, y), (0, 60, 0), 1)

    return img


# ===== MAIN LOOP =====
cap = cv2.VideoCapture(0)
angle = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # --- detect faces (target) ---
    faces = face_cascade.detectMultiScale(
        frame, scaleFactor=1.1, minNeighbors=3, minSize=(40, 40)
    )

    # draw target on camera
    target_detected = False
    for (x, y, w, h) in faces:
        cx = x + w // 2
        cy = y + h // 2
        cv2.circle(frame, (cx, cy), int(w / 2), (0, 0, 255), 3)
        target_detected = True

    # ===== ONE-TIME ALERT LOGIC =====
    if target_detected and not alert_spoken:
        play_siren()
        alert_spoken = True

    if not target_detected:
        # reset so next detection will alert again
        alert_spoken = False

    # --- radar drawing ---
    radar = create_radar_base()

    # rotating sweep line
    length = 180
    rx = int(200 + np.cos(np.deg2rad(angle)) * length)
    ry = int(200 + np.sin(np.deg2rad(angle)) * length)
    cv2.line(radar, (200, 200), (rx, ry), (0, 255, 0), 2)

    # if target: show red blip on radar
    if target_detected:
        # fixed position blip (top-right ring)
        cv2.circle(radar, (280, 120), 12, (0, 0, 255), 3)

    angle = (angle + 2) % 360

    # show windows
    cv2.imshow("RADAR", radar)
    cv2.imshow("CAMERA", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()