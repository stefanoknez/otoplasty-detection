import cv2
import matplotlib.pyplot as plt
import numpy as np

# Funkcija za ručni odabir tačaka i izračunavanje udaljenosti sa gridom
def odaberi_tačke_i_izračunaj_udaljenosti_sa_gridom(putanja_do_slike):
    # Učitaj sliku koristeći OpenCV
    img = cv2.imread(putanja_do_slike)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Prikaži sliku sa gridom
    plt.figure(figsize=(10, 10))
    plt.imshow(img_rgb)
    plt.title("Kliknite na tačke: A, B, C i D (redom)")
    
    # Dodavanje grida
    plt.grid(True, which='both', color='gray', linestyle='--', linewidth=0.5, alpha=0.5)
    
    # Omogućavanje korisniku da odabere 4 tačke
    tačke = plt.ginput(4, timeout=-1)
    plt.close()
    
    # Ekstrakcija tačaka
    A, B, C, D = tačke
    
    # Izračunavanje udaljenosti
    p = np.linalg.norm(np.array(A) - np.array(B))  # Udaljenost AB
    r = np.linalg.norm(np.array(B) - np.array(C))  # Udaljenost BC
    q = np.linalg.norm(np.array(C) - np.array(D))  # Udaljenost CD
    
    # Prikaz izračunatih udaljenosti
    print(f"Udaljenost p (AB - lijevo uvo do glave): {p:.2f} piksela")
    print(f"Udaljenost r (BC - desno uvo do nosa): {r:.2f} piksela")
    print(f"Udaljenost q (CD - lijevo uvo do nosa): {q:.2f} piksela")
    
    # Vraćanje izračunatih udaljenosti
    return p, q, r

# Primer korišćenja
putanja_do_slike = "/Users/stefanoknez/Documents/Otoplastika/DA3.webp"  # Zameijeni putanju sa putanjom do tvoje slike
p, q, r = odaberi_tačke_i_izračunaj_udaljenosti_sa_gridom(putanja_do_slike)

# Provera istaknutosti na osnovu uslova
if (p + q) / r > 0.25:
    print("Pacijent je klempav.")
else:
    print("Pacijent nije klempav.")
    
koeficijent = (p + q) / r
print("Koeficijent: ", koeficijent)
