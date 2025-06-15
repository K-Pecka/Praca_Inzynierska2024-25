# Backend

Backend aplikacji **Plannder** odpowiada za logikę biznesową, zarządzanie danymi i komunikację z aplikacją mobilną oraz panelem webowym. Został zbudowany w oparciu o framework **Django** i **Django REST Framework**.

---

## Technologie

- **Python**
- **Django**
- **Django REST Framework**
- **JWT (JSON Web Tokens)** – uwierzytelnianie
- **WebSocket (Django Channels)** – komunikacja w czasie rzeczywistym
- **PostgreSQL** – baza danych (domyślnie)

---

## Główne funkcjonalności

### Uwierzytelnianie i autoryzacja
- Logowanie użytkownika (turysta / przewodnik)
- JWT – tokeny dostępu i odświeżania
- Ochrona endpointów wymagających zalogowania

### Zarządzanie wycieczkami
- Tworzenie i edycja planów podróży (dla przewodnika)
- Pobieranie szczegółów wycieczki (dla turystów)
- Lista miejsc i aktywności w harmonogramie

### Harmonogram podróży
- Szczegółowy plan dzienny
- Przypisanie godzin, miejsc, opisu aktywności
- Możliwość aktualizacji w czasie rzeczywistym

### Budżet i wydatki
- Śledzenie budżetu i wydatków uczestników
- Rejestrowanie zaległości i płatności
- Rozliczenia między uczestnikami

### Kanały komunikacji
- Czat w ramach wycieczki
- Wymiana wiadomości między turystami a przewodnikiem
- Obsługa WebSocket przez Django Channels

### Bilety
- Przechowywanie informacji o biletach
- Dane o godzinach, cenach, statusie
- Dostępność biletów dla uczestników
---

## Uruchomienie projektu lokalnie

1. **Sklonuj repozytorium:**

   ```bash
   git clone https://github.com/K-Pecka/Praca_Inzynierska2024-25.git
   cd backend
   ```
   
2. **Stwórz i uruchom wirtualne środowisko:**

   ```bash
   python -m venv .venv
   python .venv/Script/Activate.ps1
   ```

3. **Zainstaluj zależności:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Uruchom aplikację:**

   ```bash
   python manage.py runserver
   ```

---

Rejestracja i planowanie wycieczek odbywa się na stronie:  
[https://www.plannder.com](https://www.plannder.com)
