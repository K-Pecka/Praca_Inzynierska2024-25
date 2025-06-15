# Plannder

System do organizacji i planowania podróży, zaprojektowany z myślą o turystach indywidualnych, przewodnikach oraz uczestnikach wycieczek grupowych. Projekt powstał jako odpowiedź na potrzebę prostego i intuicyjnego narzędzia, które ułatwia planowanie, zarządzanie i komunikację podczas podróży.

## Opis projektu

System składa się z trzech głównych komponentów:

- **Aplikacja internetowa** (frontend) – nowoczesna aplikacja typu SPA zbudowana przy użyciu Vue.js i Vuetify, oferująca pełny dostęp do funkcjonalności systemu z poziomu przeglądarki.

- **Aplikacja mobilna** – aplikacja mobilna oparta na Flutterze, dostępna na urządzenia z systemem Android i iOS, stanowiąca podręczne narzędzie do kontrolowania przebiegu podróży.

- **Backend** (API) – serwerowa część systemu oparta na Django oraz Django REST Framework, zapewniająca bezpieczeństwo, logikę aplikacji i komunikację z bazą danych PostgreSQL.

## Główne funkcjonalności

- Planowanie podróży i tworzenie szczegółowego harmonogramu wycieczki

- Zarządzanie budżetem, wydatkami i zaległościami uczestników

- Przechowywanie biletów

- Komunikacja między uczestnikami oraz przewodnikiem (chat, ogłoszenia)

- Obsługa grup wycieczkowych

- Synchronizacja danych między frontendem i aplikacją mobilną

## Technologie wykorzystane w projekcie 

- Frontend: Vue.js, TypeScript, Vuetify, Vue Router, Pinia, Axios

- Backend: Python, Django, Django REST Framework, PostgreSQL, JWT (SimpleJWT)

- Mobile: Flutter, Dart

- Infrastruktura i CI/CD: Heroku, GitHub Actions

- Zarządzanie projektem: ClickUp, GitHub, OneDrive

- Projektowanie UI: Figma

## Wdrożenie

Projekt został wdrożony na platformie Heroku. Automatyzacja procesu wdrażania (CI/CD) realizowana jest przy użyciu GitHub Actions, z osobnymi pipeline’ami dla frontendu i backendu. Aplikacje są synchronizowane z głównym repozytorium na GitHubie.


## Autorzy

**Mateusz Wiśniewski**

**Andrzej Ebertowski**

**Jakub Pobłocki**

**Kacper pecka**

---

**Projekt został zrealizowany w ramach pracy inżynierskiej.**
