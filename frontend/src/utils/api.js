const BASE = import.meta.env.VITE_API_BASE || '/api'

async function post(endpoint, body) {
  const res = await fetch(`${BASE}${endpoint}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Sunucu hatası')
  return data
}

async function get(endpoint) {
  const res = await fetch(`${BASE}${endpoint}`)
  const data = await res.json()
  if (!res.ok) throw new Error(data.detail || 'Sunucu hatası')
  return data
}

export const api = {
  agirlik:      (body) => post('/agirlik/hesapla', body),
  malzemeler:   ()     => get('/agirlik/malzemeler'),
  zincirBoyu:   (body) => post('/disli/zincir-boyu', body),
  trigerKayis:  (body) => post('/disli/triger-kayis-boyu', body),
  duzDisli:     (body) => post('/disli/duz-disli', body),
  kramyer:      (body) => post('/disli/kramyer', body),
  kesme:        (body) => post('/kesme/hesapla', body),
  oring:        (body) => post('/oring/hesapla', body),
  segman:       (body) => post('/oring/segman', body),
  kama:         (body) => post('/kama/hesapla', body),
  kamaTablo:    ()     => get('/kama/tablo'),
}
