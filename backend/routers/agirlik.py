from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import Literal
import math

router = APIRouter()

# kg/dm³ (= g/cm³) cinsinden özgül kütleler
MALZEME_YOGUNLUK = {
    "st37":    7.85,
    "st52":    7.85,
    "c45":     7.85,
    "42crmo4": 7.87,
    "aisi304": 7.93,
    "aisi316": 7.98,
    "aisi430": 7.75,
    "al6061":  2.70,
    "al6082":  2.71,
    "al7075":  2.83,
    "bakir":   8.96,
    "pirinc":  8.50,
    "bronz":   8.80,
    "kestamid":1.16,
    "pom":     1.41,
    "ptfe":    2.20,
    "pe1000":  0.94,
    "pa6":     1.14,
}

class AgirlikInput(BaseModel):
    malzeme: str
    form: Literal["mil", "boru", "lama", "altikose", "profil_kare", "profil_dikdortgen"]
    boy_mm: float

    # Form'a özel boyutlar (hepsi mm cinsinden)
    cap_mm:        float | None = None   # mil
    dis_cap_mm:    float | None = None   # boru
    et_mm:         float | None = None   # boru
    genislik_mm:   float | None = None   # lama / profil
    kalinlik_mm:   float | None = None   # lama / profil
    anahtar_mm:    float | None = None   # altıköşe (anahtar ağzı = s)
    profil_et_mm:  float | None = None   # profil (et kalınlığı)

    @field_validator("boy_mm", "cap_mm", "dis_cap_mm", "et_mm",
                     "genislik_mm", "kalinlik_mm", "anahtar_mm",
                     "profil_et_mm", mode="before")
    @classmethod
    def pozitif_ol(cls, v):
        if v is not None and v <= 0:
            raise ValueError("Tüm boyutlar sıfırdan büyük olmalıdır.")
        return v


def hacim_hesapla(inp: AgirlikInput) -> float:
    """Verilen forma göre hacmi dm³ cinsinden döndürür."""
    L = inp.boy_mm / 1000  # mm → dm

    if inp.form == "mil":
        if not inp.cap_mm:
            raise HTTPException(400, "Mil formu için cap_mm gerekli.")
        r = (inp.cap_mm / 1000) / 2
        return math.pi * r**2 * L

    if inp.form == "boru":
        if not inp.dis_cap_mm or not inp.et_mm:
            raise HTTPException(400, "Boru formu için dis_cap_mm ve et_mm gerekli.")
        ro = (inp.dis_cap_mm / 1000) / 2
        ri = ro - inp.et_mm / 1000
        if ri <= 0:
            raise HTTPException(400, "Et kalınlığı dış çaptan büyük olamaz.")
        return math.pi * (ro**2 - ri**2) * L

    if inp.form == "lama":
        if not inp.genislik_mm or not inp.kalinlik_mm:
            raise HTTPException(400, "Lama formu için genislik_mm ve kalinlik_mm gerekli.")
        return (inp.genislik_mm / 1000) * (inp.kalinlik_mm / 1000) * L

    if inp.form == "altikose":
        if not inp.anahtar_mm:
            raise HTTPException(400, "Altıköşe için anahtar_mm gerekli.")
        s = inp.anahtar_mm / 1000
        return (3 * math.sqrt(3) / 2) * (s / 2)**2 * L

    if inp.form in ("profil_kare", "profil_dikdortgen"):
        if not inp.genislik_mm or not inp.kalinlik_mm or not inp.profil_et_mm:
            raise HTTPException(400, "Profil için genislik_mm, kalinlik_mm ve profil_et_mm gerekli.")
        dis = (inp.genislik_mm / 1000) * (inp.kalinlik_mm / 1000)
        ic_g = (inp.genislik_mm - 2 * inp.profil_et_mm) / 1000
        ic_k = (inp.kalinlik_mm - 2 * inp.profil_et_mm) / 1000
        if ic_g <= 0 or ic_k <= 0:
            raise HTTPException(400, "Et kalınlığı profil ölçüsünden büyük olamaz.")
        return (dis - ic_g * ic_k) * L

    raise HTTPException(400, "Geçersiz form tipi.")


@router.post("/hesapla")
def agirlik_hesapla(inp: AgirlikInput):
    malzeme_key = inp.malzeme.lower().replace(" ", "").replace("-", "")
    yogunluk = MALZEME_YOGUNLUK.get(malzeme_key)
    if yogunluk is None:
        raise HTTPException(404, f"Malzeme bulunamadı: {inp.malzeme}. "
                                 f"Geçerli seçenekler: {list(MALZEME_YOGUNLUK.keys())}")
    hacim = hacim_hesapla(inp)
    agirlik_kg = hacim * yogunluk
    return {
        "agirlik_kg":   round(agirlik_kg, 4),
        "agirlik_gr":   round(agirlik_kg * 1000, 2),
        "hacim_dm3":    round(hacim, 6),
        "yogunluk":     yogunluk,
        "malzeme":      inp.malzeme,
        "form":         inp.form,
    }


@router.get("/malzemeler")
def malzeme_listesi():
    return {k: {"yogunluk_kg_dm3": v} for k, v in MALZEME_YOGUNLUK.items()}
