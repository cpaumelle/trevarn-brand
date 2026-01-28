# Trevarn Brand Guidelines

**URL:** https://brand.trevarn.com/

The official brand identity system for Trevarn and its products (Difenn, Plasen).

## Contents

| Page | Description |
|------|-------------|
| [Name](trevarn-name.html) | Etymology & pronunciation |
| [Origins](trevarn-origins.html) | Mark origins (menhirs, Vera Molnár) |
| [Logo Mark](trevarn-logo-mark.html) | Logo specs & variants |
| [Colours](trevarn-colour-palette.html) | Colour system |
| [Typography](trevarn-typography.html) | Type system |
| [Icons](trevarn-icons.html) | Icon library (92 icons) |
| [Usage](trevarn-usage.html) | Lockups, clear space, voice |

## Programmatic Access

All brand assets are available for programmatic use:

```bash
# Icons - JSON manifest
curl -s https://brand.trevarn.com/trevarn-icons.json | jq '.categories[].icons[].id'

# Icons - SVG sprite
curl -s https://brand.trevarn.com/trevarn-icons.svg

# Logo - JSON manifest
curl -s https://brand.trevarn.com/trevarn-logo.json

# Logo - SVG sprite
curl -s https://brand.trevarn.com/trevarn-logo.svg
```

## Brand Assets Summary

| Element | Specification |
|---------|--------------|
| **Primary colour** | Aour Glaz #4A6FA5 |
| **Secondary** | Aour Balan #D8A23A |
| **Tertiary** | Lin Violet #5B6B9D |
| **Display font** | IBM Plex Sans |
| **Body font** | Inter |
| **Mono font** | JetBrains Mono |
| **Mark** | Continuous outline, 2% disorder |
| **Icons** | 92 stroke-based, currentColor |

## Local Development

```bash
python3 -m http.server 8080
# Open http://localhost:8080
```

## License

Brand assets are proprietary to Trevarn. Do not use without permission.
