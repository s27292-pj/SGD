Daniel Bieliński s27292

# Mini prezentacja

## Reflex inferno - Gra w stylu bullet hell / touhou


RefleX Inferno to dynamiczna gra zręcznościowa typu "bullet hell" stworzona w Pythonie z użyciem biblioteki Pygame. Gracz musi unikać kolorowych pocisków poruszających się po ekranie, wykorzystując swoje refleksy i umiejętności strategiczne.

## Jak Grać
1. Start: Naciśnij SPACJĘ na ekranie powitalnym
2. Menu: Wybierz poziom (1-3) lub tryb gry
3. Wybór skina: Przejdź przez dostępne skiny (A/D)
4. Gra: Unikaj kolorowych pocisków jak najdłużej
5. Pauza: Naciśnij P w trakcie gry
6. Restart: Naciśnij R po przegranej
7. Sterowanie dźwiękiem: [m = mute, (-) = volume down, (+) = volume up]

# Funkcjonalności (17)

### Sterowanie i interakcja
- obsługa klawiatury - ruchy postaci, ruchy w menu
- wykrywanie kolizji - bullets
- moliwość sterowania więcej niz jedna postacia - 2 graczy
- local multiplayer
- wybór skina przed grą


### Logika gry
- system punktacji - punkty za przetrwanie
- mechanika levelowania - odblokowywanie skinów za xp
- losowe generowanie pocisków na poziomy

### Grafika i Animacja
- prosty interfejs uytkownika

### Dźwięk i muzyka
- Muzyka w tle, levele, main screen, death screen
- Rózne dźwięki w zalezności od sytuacji
- Włączenie wyłączenie dźwięku oraz zmiana głośności - M=mute, +/-=volume

### Struktura gry
- Ekran powitalny z tytułem gry
- Menu główne z wyborem poziomów, wyborem skinów
- Ekran przegranej
- Przechowywanie stanu gry, zapisywanie high scores, zapisywanie XP oraz skinów
- Ekran Pauzy - P=pauza ingame
