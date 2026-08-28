# Explainable Resume–Job Matcher

A local Python tool that compares resume text with a job description and shows exactly why the match score changed.

## What I built

- A tokenizer that normalizes useful terms and removes common stop words
- Frequency-weighted scoring so repeated job requirements matter more
- Separate matched and missing keyword lists
- Three readable verdict bands: needs tailoring, good foundation and strong match
- JSON output that can be saved for another workflow

The project uses no API key or paid service. Its output is deterministic for the same two text files.

## Example result

The included sample files currently return a **42.9%** match, nine matched terms and twelve missing terms. The recommendation explicitly tells the user to add only skills they genuinely have and can support with project evidence.

## Run and verify

```bash
python app.py sample_resume.txt sample_job.txt
python test.py
```

The tests cover tokenization, matched/missing terms, a realistic score range and rejection of a job description with no useful keywords.

## Files

- `app.py` — matching and CLI logic
- `sample_resume.txt` — synthetic resume text
- `sample_job.txt` — synthetic job description
- `test.py` — automated behaviour checks

## Scope

This is an explainable keyword-coverage baseline, not a claim to reproduce a commercial ATS or predict hiring decisions.

[Back to flagship case studies](../PORTFOLIO_SHOWCASE.md)
