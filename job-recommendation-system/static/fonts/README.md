# Offline font assets

The application serves both typefaces from this folder, with no Google Fonts or CDN request at runtime.

| Typeface | Use | Original source | License |
| --- | --- | --- | --- |
| Manrope variable, 200–800 | Interface, headings, chart labels | [Google Fonts / Manrope](https://github.com/google/fonts/tree/main/ofl/manrope) | [SIL OFL 1.1](MANROPE-OFL.txt) |
| Fraunces italic variable, 100–900 | Editorial headline accents | [Google Fonts / Fraunces](https://github.com/google/fonts/tree/main/ofl/fraunces) | [SIL OFL 1.1](FRAUNCES-OFL.txt) |

Retrieved on 7 October 2026. Original variable TTFs were repackaged as WOFF2 with FontTools and Brotli; the full glyph sets and font metadata are preserved. `font-display: swap` keeps text readable while the local font loads.

Manrope is preloaded. Fraunces loads only when the page uses an italic accent. System-font fallbacks remain available.
