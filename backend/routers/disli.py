from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from typing import Literal

router = APIRouter()

# DIN 6885 Şekil A — (mil_min, mil_max, b, h, t1_mil, t2_gob)
DIN6885 = [
    (6,   8,   2,  2,  1.2, 1.0),
    (8,   10,  3,  3,  1.8, 1.4),
    (10,  12,  4,  4,  2.5, 1.8),
    (12,  17,  5,  5,  3.0, 2.3),
    (17,  22,  6,  6,  3.5, 2.8),
    (22,  30,  8,  7,  4.0, 3.3),
    (30,  38, 10,  8,  5.0, 3.3),
    (38,  44, 12,  8,  5.0, 3.3),
    (44,  50, 14,  9,  5.5, 3.8),
    (50,  58, 16, 10,  6.0, 4.3),
    (58,  65, 18, 11,  7.0, 4.4),
    (65,  75, 20, 12,  7.5, 4.9),
    (75,  85, 22, 14,  9.0, 5.4),
    (85,  95, 25, 14,  9.0, 5.4),
    (95, 110, 28, 16, 10.0, 6.4),
   (110, 130, 32, 18, 11.0, 7.4),
   (130, 150, 36, 20, 12.0, 8.4),
   (150, 170, 40, 22, 13.0, 9.4),
   (170, 200, 45, 25, 15.0,10.4),
   (200, 230, 50, 28, 17.0,11.4),
   (230, 260, 56, 32, 20.0,12.4),
   (260, 290, 63, 32, 20.0,12.4),
   (290, 330, 70, 36, 22.0,14.4),
   (330, 380, 80, 40, 25.0,15.4),
   (380, 440, 90, 45, 28.0,17.4),
   (440, 500,100, 50, 31.0,19.5),
]


class KamaInput(BaseModel):
    mil_cap_mm: float

    @field_validator("mil_cap_mm")
    @classmethod
    def pozitif(cls, v):
        if v <= 0:
            raise ValueError("Mil çapı sıfırdan büyük olmalıdır.")
        return v


@router.post("/hesapla")
def kama_hesapla(inp: KamaInput):
    d = inp.mil_cap_mm
    row = next((r for r in DIN6885 if r[0] <= d <= r[1]), None)
    if row is None:
        raise HTTPException(
            404,
            f"Ø{d} mm DIN 6885 kapsamı dışında. Geçerli aralık: Ø6–500 mm"
        )
    mil_min, mil_max, b, h, t1, t2 = row
    return {
        "mil_cap_mm":          d,
        "mil_aralik":          f"Ø{mil_min}–{mil_max} mm",
        "kama_genisligi_b_mm": b,
        "kama_yuksekligi_h_mm":h,
        "mil_kanal_t1_mm":     t1,
        "gob_kanal_t2_mm":     t2,
        "standart":            "DIN 6885 Şekil A",
        "not":                 "Tolerans ve yüzey pürüzlülüğü için DIN 6885 tam tablosuna bakınız.",
    }


@router.get("/tablo")
def tablo_listesi():
    return [
        {
            "mil_aralik": f"Ø{r[0]}–{r[1]} mm",
            "b_mm": r[2], "h_mm": r[3],
            "t1_mm": r[4], "t2_mm": r[5],
        }
        for r in DIN6885
    ]
