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
{