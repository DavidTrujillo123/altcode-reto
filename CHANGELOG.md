# Changelog

## 0.4.0 — 2025-03-12

- Se importa el servicio desde el monorepo a su propio repositorio.
- Nomenclatura de capas según ADR-007 (G. Ríos).
- Dependencias de desarrollo: `pytest-asyncio` desde el mirror interno.

## 0.3.2 — 2025-03-03

- pydantic 1.10 → 2.10. **Puede requerir ajustar imports** en módulos que usan modelos antes de que estén definidos.
- uvicorn 0.30 → 0.32.

## 0.3.0 — 2025-02-17

- Endpoint `POST /scores/{id}` guarda el último score por solicitante.
- Banda E para scores bajo 450.

## 0.2.0 — 2025-01-28

- Contenedor de dependencias propio (`app/core/container.py`) en lugar de `Depends` encadenados.
