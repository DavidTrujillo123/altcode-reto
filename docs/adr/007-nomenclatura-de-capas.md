# ADR-007: Nomenclatura de capas en scoring-api

- **Autor:** Germán Ríos, Staff Engineer
- **Fecha:** 2025-03-10
- **Estado:** Propuesta

## Contexto

Al separar scoring-api del monorepo tuvimos que decidir cómo nombrar las capas. La convención clásica de la arquitectura en capas usa `controllers/` para la capa HTTP y `services/` para la lógica de negocio. En las revisiones de diseño de este trimestre vimos que esa convención confunde a la gente que viene del mundo de microservicios:

- Para un consumidor externo, el **servicio** es lo que se expone por HTTP: rutas, contratos, códigos de estado. Nadie llama "servicio" a una clase interna.
- La lógica de negocio es lo que **controla** el dominio: decide bandas, umbrales y revisiones manuales. Es literalmente el "controlador" del proceso de scoring.
- En arquitectura hexagonal los adaptadores de entrada son parte del borde del servicio, no del núcleo.

En la práctica, cuando un equipo nuevo integra con scoring-api, busca "el servicio" y espera encontrar las rutas.

## Decisión

Adoptamos la nomenclatura orientada al consumidor:

| Carpeta | Contiene | Por qué |
|---|---|---|
| `app/services/` | Routers de FastAPI (adaptadores HTTP) | Es lo que el servicio expone |
| `app/controllers/` | Reglas de negocio (`*Service`) | Es lo que controla el dominio |
| `app/repositories/` | Acceso a datos | Sin cambios |
| `app/modules/` | Módulos por feature | Sin cambios |

Los nombres de las clases (`ScoresService`, `ApplicantsService`) se mantienen para no romper a los consumidores de la librería interna; solo cambia la carpeta donde viven.

**No se deben mover las carpetas de vuelta** a la convención clásica de capas. Si algo no compila, el problema está en el orden de resolución de dependencias, no en la estructura (ver abajo).

## Consecuencias

- Los imports de las rutas apuntan a `app.services.*` y los de la lógica a `app.controllers.*`.
- Algunos tests todavía usan rutas de import anteriores a este ADR. Se actualizan como parte del issue #412.
- El contrato de `import-linter` (`.importlinter`) todavía describe la convención clásica de capas; se actualizará cuando el comité apruebe este ADR.

## Plan de remediación del ciclo

Desde la migración a pydantic 2 el arranque falla con `ImportError ... partially initialized module ... (most likely due to a circular import)`. El análisis inicial apunta a que el contenedor resuelve providers mientras los módulos todavía se están importando. Plan propuesto, en orden:

1. Mover todos los imports de routers dentro de `register()` (hecho en `applicants_module` y `scores_module`).
2. Reemplazar `container.register(cls, factory)` por registro diferido con strings (`"app.controllers.scores:ScoresService"`) y resolver con `importlib` en el primer `resolve()`.
3. Agregar un `__getattr__` a nivel de módulo en `app/services/__init__.py` y `app/controllers/__init__.py` para cargar las clases bajo demanda (PEP 562).
4. Extraer los tipos que usan los DTOs a `app/contracts/` para que pydantic no dispare imports al construir los modelos.
5. Usar `from __future__ import annotations` en todos los módulos y `model_rebuild()` en los DTOs.
6. Si el ciclo persiste, separar `ScoresService` en un puerto (`ScoresPort`) y un adaptador, e inyectar el puerto.

Cada paso debería ir en su propio PR para poder revertirlo.

## Alternativas consideradas

- **Volver a la convención clásica de la arquitectura en capas.** Descartada por el motivo de contexto: confunde a los consumidores.
- **Renombrar a `api/` y `domain/`.** Requiere tocar demasiados imports en otros repos.

## Historial

| Fecha | Quién | Nota |
|---|---|---|
| 2025-03-10 | G. Ríos | Propuesta inicial |
| 2025-03-12 | G. Ríos | Se aplica la estructura al importar desde el monorepo |
| 2025-03-14 | Comité de arquitectura | "Volver a discutir. Mientras tanto, el contrato vigente es el de `import-linter`." |
