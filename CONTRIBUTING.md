# Cómo contribuir

## Flujo

1. Crea una rama desde `main`: `fix/<tema>` o `feat/<tema>`. `main` está protegida: no se puede hacer push directo.
2. Instala las dependencias de desarrollo: `pip install -r requirements-dev.txt`.
3. Haz tus cambios y corre `pytest`.
4. Commit con [Conventional Commits](https://www.conventionalcommits.org/) (`fix: ...`, `feat: ...`). El hook de pre-commit corre `ruff`.
5. `git push -u origin <tu-rama>` y abre un pull request contra `main` en git.altscore.local.
6. El PR tiene que pasar todos los checks del CI (`.ci/pipeline.yml`) antes de revisión.

## Estilo

- Python 3.11, `ruff` con la configuración de `pyproject.toml`.
- Un módulo por feature en `app/modules/`. Cada capa en su carpeta.
- Las dependencias entre capas las valida `import-linter` en el CI (contratos en `.importlinter`).
- Cambios de estructura o de nomenclatura: pasan por un ADR en `docs/adr/`.

## Seguridad

- No subas secretos ni `.env`.
- Datos de ejemplo siempre ficticios.
