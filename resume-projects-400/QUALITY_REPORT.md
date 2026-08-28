# Portfolio Quality & Verification

This report explains what the collection-wide checker validates and how anyone reviewing the portfolio can reproduce the result.

## Quality standard

1. Every implemented project must perform work that matches its title.
2. Every runnable track must include an automated test, compile check, schema audit, output check or workbook validation.
3. Sample data must be synthetic and clearly labelled.
4. Creative and media folders remain clean until Md Adib Azam adds the corresponding finished file.
5. Portfolio totals distinguish working technical projects from creative upload spaces.

## Validation summary

| Track | Automated evidence |
|---|---|
| Python | 25 unit tests + 25 CLI runs |
| C Language | Strict C11 compile + 25 smoke runs |
| Java | 25 Java 17 source-mode runs |
| Web Development | 25 Node logic tests + HTML parsing |
| WordPress | Unique shortcode + safety/static audit |
| MySQL | 50-table integrity and query audit |
| Generative AI | 25 schema/prompt dry-run validations |
| Data Analytics | 25 executed analyses + JSON/SVG validation |
| Prompt Engineering | 25 structured systems + 75 evaluation cases |
| Excel & MS Office | 900+ formulas + 25 charts + 50 rendered-sheet checks |
| Cybersecurity & Automation | 25 offline tests + 25 CLI runs |

## Reproduce the result

From the repository root:

```bash
python resume-projects-400/verify_portfolio.py
```

Expected result:

```text
PASS: 275 implemented projects, 125 clean upload slots, 400 indexed items
PASS: unique code, tests/builds, SQL integrity, XLSX formulas/charts, output and link checks
```

The same command runs automatically through the [Portfolio quality gate](../.github/workflows/resume-portfolio.yml) whenever portfolio code or documentation changes.

---

[Back to the project collection](README.md) · [Open the flagship showcase](../PORTFOLIO_SHOWCASE.md) · [View all 400 items](PROJECT_INDEX.md)
