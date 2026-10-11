# GeoJSON-to-SVG Architecture Review

## Problem and proposed approach

The converter is concentrated in a shared geometry/model module, while five
versioned converter modules contain competing processing algorithms. Recommend
consolidating the core around an explicit conversion pipeline, isolating data
loading, geometry operations, and SVG output, and removing process-global
geometry state so conversions are independent and testable.

## Prioritized recommendations

1. **Make conversion state instance-owned.** Move `POINTS`, `POLYGONS`,
   `MULTIPOLYGONS`, and `PARENTS` out of module scope into a conversion/model
   context. Give each conversion independent ID allocation and ownership, and
   define map combination without cross-instance registry side effects.
2. **Split `common.py` by responsibility.** A reasonable class/module layout:
   `GeometryContext` plus `Point`/`Polygon`/`MultiPolygon` in a model module;
   a GeoJSON reader and land metadata/configuration module; geometry transforms
   and topology operations in separate modules; and an SVG renderer/output
   module. Retain a small `Converter`/pipeline facade.
3. **Select and name one supported boundary-processing implementation.**
   Replace `geojson2svg_good0` … `good4` with a named strategy or pipeline
   implementation, and move unsuccessful experiments out of the supported
   import path. Reconcile the contradictory status notes: `main.py` imports
   `good4`, while its comments call `good0` best and report failures in both.
4. **Make pipeline stages explicit and ordered.** Represent loading,
   coordinate projection/scaling, simplification/rounding, shared-border
   reconciliation, validation, and rendering as named stages with documented
   inputs/invariants. Keep stage options such as precision in configuration
   rather than scattered module constants.
5. **Separate geometry algorithms from mutation and I/O.** Prefer algorithms
   that return edits/results, with one owner applying changes and checking
   topology invariants. Route progress and diagnostics through the existing
   reporting abstraction rather than direct `print()` calls.
6. **Accelerate pair discovery.** Replace exhaustive multipolygon/polygon and
   point-pair scans with a spatial index or sweep/grid strategy after defining
   correctness tests and representative benchmarks. Keep a simple fallback for
   small datasets if measurements justify it.
7. **Validate GeoJSON at the input boundary.** Check feature properties,
   geometry types, coordinate nesting, rings, empty geometries, and identifier
   collisions before creating model objects; report contextual errors rather
   than relying on assertions or `SystemExit`.
8. **Make paths and side effects explicit.** Remove `os.chdir()` from
   `MapObj` construction; accept or derive input/output `Path` values without
   changing process-wide working-directory state. Separate generation from
   writing so output can be tested in memory.
9. **Build a focused automated test suite before consolidation.** Replace the
   current data-dependent manual `test()` entry point with synthetic fixtures
   for geometry parsing, projection, simplification, shared-border handling,
   map combination, and SVG output; add regression fixtures for the known
   broken/slow city cases.

## Proposed class/module direction

- `LandConfig`: immutable input/output metadata (names, dimensions, ID/name/
  parent fields, and processing options).
- `GeometryContext`: owns geometry objects and ID registries for one conversion.
- `Point`, `Polygon`, `MultiPolygon`, and `MapModel`: represent geometry and
  hierarchy without file access or SVG rendering.
- `GeoJSONReader`: validates and loads features into a `MapModel`.
- `ConversionPipeline` plus named stage/strategy objects: coordinates
  transforms, simplification, and border reconciliation.
- `SvgRenderer`: serializes a validated model; a separate writer handles paths.

## Notes

- This is an architecture-only review; no repository files were changed.
- Recommendations are ordered to put correctness/isolation before performance.
- Preserve the existing command behavior and generated SVG output during any
  later migration; compare outputs and benchmarks before removing legacy code.
