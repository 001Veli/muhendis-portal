from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import List

router = APIRouter()


class Parca(BaseModel):
    boy_mm: float
    adet: int

    @field_validator("boy_mm")
    @classmethod
    def pozitif_boy(cls, v):
        if v <= 0:
            raise ValueError("Parça boyu sıfırdan büyük olmalıdır.")
        return v

    @field_validator("adet")
    @classmethod
    def pozitif_adet(cls, v):
        if v < 1:
            raise ValueError("Adet en az 1 olmalıdır.")
        return v


class KesmeInput(BaseModel):
    stok_boy_mm: float          # standart stok malzeme boyu (ör. 6000 mm)
    parcalar: List[Parca]       # kesilecek parçalar

    @field_validator("stok_boy_mm")
    @classmethod
    def stok_pozitif(cls, v):
        if v <= 0:
            raise ValueError("Stok boyu sıfırdan büyük olmalıdır.")
        return v


def first_fit_decreasing(stok: float, talep: list[tuple[float, int]]) -> list[list[float]]:
    """
    First-Fit Decreasing (FFD) algoritması.
    talep: [(boy, adet), ...] — büyükten küçüğe sıralanmış.
    Döndürür: her stok malzeme için kesilen parça boyları listesi.
    """
    # Talebi düzleştir: her parçayı ayrı ayrı listele, büyükten küçüğe sırala
    parcalar = sorted(
        [boy for boy, adet in talep for _ in range(adet)],
        reverse=True
    )
    kutukler: list[list[float]] = []
    kalan: list[float] = []

    for parca in parcalar:
        if parca > stok:
            raise HTTPException(
                400,
                f"{parca} mm'lik parça, stok boyu {stok} mm'den uzun. Kesilemez."
            )
        # Mevcut stok malzemelere sığıyor mu?
        yerlestirildi = False
        for i, k in enumerate(kalan):
            if k >= parca:
                kutukler[i].append(parca)
                kalan[i] -= parca
                yerlestirildi = True
                break
        if not yerlestirildi:
            kutukler.append([parca])
            kalan.append(stok - parca)

    return kutukler, kalan


@router.post("/hesapla")
def kesme_hesapla(inp: KesmeInput):
    if not inp.parcalar:
        raise HTTPException(400, "En az bir parça girilmelidir.")

    talep = [(p.boy_mm, p.adet) for p in inp.parcalar]
    kutukler, kalan_list = first_fit_decreasing(inp.stok_boy_mm, talep)

    toplam_stok = len(kutukler) * inp.stok_boy_mm
    toplam_kullanim = sum(sum(k) for k in kutukler)
    toplam_fire = sum(kalan_list)
    fire_orani = toplam_fire / toplam_stok * 100 if toplam_stok > 0 else 0

    plan = []
    for i, (kesimler, kalan) in enumerate(zip(kutukler, kalan_list)):
        plan.append({
            "stok_no":     i + 1,
            "kesimler_mm": [round(k, 1) for k in kesimler],
            "kullanim_mm": round(sum(kesimler), 1),
            "fire_mm":     round(kalan, 1),
        })

    return {
        "algoritma":         "First-Fit Decreasing (FFD)",
        "stok_boy_mm":       inp.stok_boy_mm,
        "kullanilan_stok":   len(kutukler),
        "toplam_stok_mm":    round(toplam_stok, 1),
        "toplam_kullanim_mm":round(toplam_kullanim, 1),
        "toplam_fire_mm":    round(toplam_fire, 1),
        "fire_orani_yuzde":  round(fire_orani, 2),
        "kesim_plani":       plan,
    }
