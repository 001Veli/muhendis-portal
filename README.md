# ⬡ Mühendis Portal

Apple estetiğinde, Python FastAPI backend ile çalışan mühendislik hesaplama portalı.

## Proje Yapısı

```
muhendis-portal/
├── backend/          ← Python FastAPI
│   ├── main.py       ← Uygulama giriş noktası
│   ├── routers/
│   │   ├── agirlik.py   ← Ağırlık hesaplama
│   │   ├── disli.py     ← Dişli hesaplamaları
│   │   ├── kesme.py     ← Kesme listesi optimizasyonu
│   │   ├── oring.py     ← O-Ring & segman
│   │   └── kama.py      ← Kama kanalı DIN 6885
│   └── requirements.txt
└── frontend/         ← React + Vite + Tailwind
    ├── src/
    │   ├── App.jsx
    │   ├── pages/       ← Sayfa bileşenleri
    │   ├── components/  ← Ortak bileşenler
    │   └── utils/api.js ← API çağrıları
    └── package.json
```

---

## Kurulum (İlk Kez)

### Gereksinimler
- [Python 3.11+](https://www.python.org/downloads/) — `python --version` ile kontrol edin
- [Node.js 20+](https://nodejs.org/) — `node --version` ile kontrol edin
- [Git](https://git-scm.com/) — `git --version` ile kontrol edin

---

### 1. Projeyi Klonlayın

```bash
git clone https://github.com/KULLANICI_ADINIZ/muhendis-portal.git
cd muhendis-portal
```

---

### 2. Backend Kurulumu

```bash
cd backend

# Sanal ortam oluştur (öneri: her projede ayrı ortam)
python -m venv venv

# Sanal ortamı aktif et
# Windows:
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

# Bağımlılıkları yükle
pip install -r requirements.txt

# Sunucuyu başlat
uvicorn main:app --reload --port 8000
```

Tarayıcıda `http://localhost:8000/docs` adresine giderek API belgelerini görebilirsiniz.

---

### 3. Frontend Kurulumu (yeni terminal)

```bash
cd frontend

# Bağımlılıkları yükle
npm install

# Geliştirme sunucusunu başlat
npm run dev
```

Tarayıcıda `http://localhost:5173` adresini açın.

---

## Günlük Kullanım

Her gün çalıştırmak için iki terminal açın:

**Terminal 1 — Backend:**
```bash
cd backend
source venv/bin/activate   # (Windows: venv\Scripts\activate)
uvicorn main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

---

## API Endpointleri

| Modül     | Endpoint                  | Method |
|-----------|---------------------------|--------|
| Ağırlık   | `/api/agirlik/hesapla`    | POST   |
| Malzemeler| `/api/agirlik/malzemeler` | GET    |
| Zincir    | `/api/disli/zincir-boyu`  | POST   |
| Triger    | `/api/disli/triger-kayis-boyu` | POST |
| Düz Dişli | `/api/disli/duz-disli`    | POST   |
| Kramyer   | `/api/disli/kramyer`      | POST   |
| Kesme     | `/api/kesme/hesapla`      | POST   |
| O-Ring    | `/api/oring/hesapla`      | POST   |
| Segman    | `/api/oring/segman`       | POST   |
| Kama      | `/api/kama/hesapla`       | POST   |
| Kama Tablo| `/api/kama/tablo`         | GET    |

Tam API belgesi için: `http://localhost:8000/docs`

---

## Yeni Modül Eklemek

1. `backend/routers/` altına yeni bir `.py` dosyası oluşturun
2. `backend/main.py` içine `include_router` satırı ekleyin
3. `frontend/src/utils/api.js` içine endpoint fonksiyonu ekleyin
4. `frontend/src/pages/` altına yeni sayfa bileşeni oluşturun
5. `frontend/src/App.jsx` içine route ekleyin

---

## Standartlar

- **DIN 6885** — Kama kanalları (Ø6–500 mm, 26 adım)
- **DIN 471** — Mil segmanı (Ø8–100 mm)
- **ISO 3601 / DIN 3771** — O-Ring seçimi
- **ISO 606** — Zincir dişli hesabı
