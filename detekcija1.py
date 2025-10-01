import cv2
import dlib
import numpy as np

# Inicijalizujem dlib i OpenCV
detektor = dlib.get_frontal_face_detector()                                     
prediktor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")       

# Parametri
real_face_height = 15.0  # Prosječna visina lica u cm, bilo bi mzd bolje u mm   
focal_length = 800  # Žižna daljina (prilagođava se shodno kameri)              

# Pokrecem kameru
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detektor(gray)

    for face in faces:
        landmarks = prediktor(gray, face)

        # Ovđe koristim ključne tačke glave kao referentne tačke za uši
        jaw_left = landmarks.part(1)  # Lijeva strana vilice
        jaw_right = landmarks.part(15)  # Desna strana vilice
        
        # Približno postavljam tačke krajnjih ivica ušiju na osnovu vilice
        left_ear_edge = (jaw_left.x - 15, jaw_left.y)  # Ručno dodavanje tačke krajnje lijeve ušne školjke
        right_ear_edge = (jaw_right.x + 15, jaw_right.y)  # Ručno dodavanje tačke krajnje desne ušne školjke

        # Ručno postavljam vertikale linije ka glavi, kao referentne tačake za udaljenost
        left_face_point = (face.left(), jaw_left.y)  # Lijeva ivica lica na istoj visini kao lijeva ušna školjka
        right_face_point = (face.right(), jaw_right.y)  # Desna ivica lica na istoj visini kao desna ušna školjka

        # Crtam paralelne linije između krajnjih tačaka ušiju i glave
        cv2.line(frame, left_ear_edge, left_face_point, (255, 0, 0), 2)  # Lijeva paralelna linija
        cv2.line(frame, right_ear_edge, right_face_point, (255, 0, 0), 2)  # Desna paralelna linija

        # Računam normalnu udaljenost krajnjih ivica ušiju od glave
        distance_left = np.linalg.norm(np.array(left_ear_edge) - np.array(left_face_point))
        distance_right = np.linalg.norm(np.array(right_ear_edge) - np.array(right_face_point))

        # Prikaz udaljenosti između ušiju i glave
        cv2.putText(frame, f"Lijevo uvo: {distance_left:.2f} cm", (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Desno uvo: {distance_right:.2f} cm", (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Provjeravam klempavost ušiju (ako je razdaljina veća od 2 cm)
        klempavost_left = "Klempavo" if distance_left > 2 else "Normalno"
        klempavost_right = "Klempavo" if distance_right > 2 else "Normalno"

        # Prikaz rezultata klempavosti
        cv2.putText(frame, f"Lijevo uvo: {klempavost_left}", (10, 190), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(frame, f"Desno uvo: {klempavost_right}", (10, 230), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Izračunavanje realne udaljenosti lica od kamere
        jaw = landmarks.part(8)  # Brada
        forehead = landmarks.part(27)  # Čelo
        
        # Računam visinu lica u pikselima
        face_height_pixels = forehead.y - jaw.y

        # Prikaz vrijednosti u terminalu radi debagovanja, jer jbg može mi se, jaka mašina
        print("Čelo Y:", forehead.y, "Jaw Y:", jaw.y)
        print("Visina lica u pikselima:", face_height_pixels)

        # Procjenjujem udaljenost, nidje ni online nema prosto ocjenjivanje udaljenosti 
        distance = None
        if face_height_pixels > -500:  # Provjeravam validnu visinu lica (>0) ali na osnovu goreprikazanih 
            # vrijednosti u terminalu vidim da javlja grešku i ulazeći u else ispisuje N/A, pa sam stavio > -500
            # Formula za izračunavanje udaljenosti (fala kurcu radi)
            distance = (real_face_height * focal_length) / face_height_pixels
            distance_cm = abs(distance)  # Udaljenost u centimetrima, ispisuje -, pa zato ide abs
            cv2.putText(frame, f"Udaljenost: {distance_cm:.2f} cm", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Udaljenost: N/A", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Prikaz slike
    cv2.imshow("Detekcija klempavosti i udaljenosti", frame)

    # Prekini ako je pritisnuto 'q' (quit)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
