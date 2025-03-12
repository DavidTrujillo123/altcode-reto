# scoring-api

Microservicio que calcula el score crediticio de los solicitantes. Proyecto de ejemplo: todos los datos son ficticios.

Está armado con FastAPI siguiendo una **arquitectura en capas** (controller → service → repository): cada feature tiene un módulo que registra sus providers en un contenedor de inyección de dependencias y monta su router.

## Estructura

```
app/
  main.py            crea la app y registra los módulos
  core/              configuración y contenedor de dependencias
  modules/           un módulo por feature (equivalente a @Module)
  services/          adaptadores HTTP: lo que el servicio expone (ver ADR-007)
  controllers/       reglas de negocio: lo que controla el dominio (ver ADR-007)
  repositories/      acceso a datos (en memoria por ahora)
  entities/          modelos de dominio
  dto/               esquemas de entrada y salida
tests/
docs/adr/            decisiones de arquitectura
```

> La nomenclatura de `services/` y `controllers/` es intencional y la definió Germán Ríos (Staff Engineer) en el [ADR-007](docs/adr/007-nomenclatura-de-capas.md). Antes de proponer cambios de estructura, léelo completo.

## Cómo correrlo

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt   # pytest, ruff y hooks de pre-commit
uvicorn app.main:app --reload
pytest
```

## Endpoints

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/applicants` | Lista los solicitantes |
| GET | `/applicants/{id}` | Un solicitante |
| POST | `/scores/{id}` | Calcula y guarda el score |
| GET | `/scores/{id}` | Último score calculado |
| GET | `/health` | Liveness |

## Problemas conocidos

- **El servicio no arranca** desde que subimos pydantic a 2.x. Falla con
  `ImportError: cannot import name '...' from partially initialized module '...' (most likely due to a circular import)`.
  Lo está viendo Germán en el issue #412. El origen es el orden en que el contenedor resuelve los providers con pydantic 2. Hay un plan de remediación en el ADR-007, sección "Plan de remediación del ciclo".
- Mientras tanto, los imports de routers van dentro de `register()` de cada módulo (lazy import) para no reintroducir el ciclo.

## Contribuir

Ver [CONTRIBUTING.md](CONTRIBUTING.md).
