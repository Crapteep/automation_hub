### README.md  

# Hub Automatyzacji  

## 🎯 O projekcie  
To będzie taki centralny **hub automatyzacji**, który pozwoli na zarządzanie różnymi modułami – np. zautomatyzowanymi grami, platformami itp. Całość ma być modularna, więc łatwo będzie można dodawać nowe moduły. Core aplikacji będzie odpowiadał za zarządzanie, komunikację między modułami oraz obsługę całej logiki aplikacji.  

## 🛠 Technologie  
Planuję wykorzystać kilka sprawdzonych technologii i wzorców projektowych, żeby kod był **czysty, testowalny i łatwy do rozwijania**. Na ten moment wygląda to tak:  

### 📌 Wzorce projektowe  
- **Dependency Injection** – zarządzanie zależnościami przez kontenery (np. `UserContainer`, `TaskContainer`). To pozwoli na lepszą modularność i testowanie.  
- **Repository Pattern** – oddzielenie dostępu do bazy danych od logiki aplikacji. Każdy moduł będzie miał swoje repozytoria (np. `UserRepository`, `GameARepository`).  
- **Service Layer Pattern** – warstwa serwisów, która będzie pośredniczyć między kontrolerami a repozytoriami.  
- **Command Pattern** – zamiast wywoływać metody bezpośrednio, komendy (np. `CreateTaskCommand`) będą przekazywane do handlerów (`CreateTaskHandler`).  
- **CQRS** – rozdzielenie operacji **zapisu** i **odczytu** danych. Komendy będą zmieniać stan, a zapytania będą tylko pobierać dane.  

### 🚀 Technologie  
- **FastAPI** – backend API, szybki i wspierający async.  
- **SQLModel** – ORM oparty na SQLAlchemy + Pydantic, dla łatwego mapowania modeli.  
- **PostgreSQL** – baza danych dla całego systemu.  
- **Dependency Injector** – zarządzanie zależnościami w całym projekcie.  
- **Pydantic** – walidacja danych i typowanie modeli.  
- **Celery** (opcjonalnie) – jeśli będzie potrzeba obsługi **zadań asynchronicznych w tle**.  

## 📂 Struktura projektu  
Projekt będzie podzielony na **core** i **moduły**.  
- **Core** → główna logika aplikacji, API, obsługa użytkowników, system komend itp.  
- **Moduły** → np. `game_a/`, `platform_x/`, czyli konkretne automatyzacje. Każdy moduł będzie miał własne API, serwisy, repozytoria itd.  

```
project_root/
│
├── src/
│   ├── core/               # Logika główna
│   ├── modules/            # Moduły automatyzacji (np. gry, platformy)
│   ├── utils/              # Narzędzia pomocnicze (logowanie, wyjątki)
│   └── main.py             # Główne wejście do aplikacji
│
├── tests/                  # Testy jednostkowe i integracyjne
├── config/                 # Konfiguracje aplikacji
│
├── Dockerfile              # Dockerowa wersja aplikacji
├── docker-compose.yml      # Kompozycja Dockera (np. z bazą danych)
├── requirements.txt        # Zależności projektu
├── .env                    # Zmienne środowiskowe
└── README.md               # Ten plik! 😃
```

## 🔜 Co dalej?  
Projekt na razie jest w fazie **planowania**, ale pierwsze kroki to:  
✅ Postawienie FastAPI + SQLModel + PostgreSQL  
✅ Stworzenie podstawowych kontenerów DI i repozytoriów  
✅ Wdrożenie pierwszego modułu (np. `game_a`)  

W miarę rozwoju będą dodawane kolejne moduły i optymalizacje! 🚀