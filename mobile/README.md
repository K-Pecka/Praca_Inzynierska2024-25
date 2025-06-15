# Aplikacja mobilna

Aplikacja mobilna systemu **Plannder** to podręczne narzędzie do kontrolowania przebiegu podróży. Działa w oparciu o backend napisany w Django i integruje się z panelem webowym dostępnym pod adresem:  
[https://www.plannder.com](https://www.plannder.com)

---

## Funkcje aplikacji

- logowanie na konto turysty i przewodnika
- Przegląd zaplanowanej wycieczki
- Podgląd planu podróży
- Monitorowanie budżetu, wydatków i zaległości
- Kanały komunikacji w wycieczkach organizowanych przez przewodnika
- Obsługa biletów

---

## Technologie

- **Flutter** (front-end mobilny)
- **Dart**
- **Django REST API** (back-end)
- Autoryzacja za pomocą JWT
- WebSocket (komunikacja w czasie rzeczywistym)

---

## Uruchomienie projektu lokalnie

1. **Sklonuj repozytorium:**

   ```bash
   git clone https://github.com/K-Pecka/Praca_Inzynierska2024-25.git
   cd mobile
   ```

2. **Zainstaluj zależności:**

   ```bash
   flutter pub get
   ```

3. **Uruchom aplikację:**

   ```bash
   flutter run
   ```

4. **Zbuduj plik APK:**

   ```bash
   flutter build apk
   ```

---

Rejestracja i planowanie wycieczek odbywa się na stronie:  
[https://www.plannder.com](https://www.plannder.com)
