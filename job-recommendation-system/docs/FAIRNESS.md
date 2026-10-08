# Fairness and bias review

## Features considered

| Attribute | Ranking use / reason |
|---|---|
| Skills, projects, role interests | Professional compatibility; dictionary and text similarity |
| Experience years | Explicit minimum-experience fit, never inferred age |
| Education qualification level | Employer requirement fit; no institution/prestige feature |
| Desired location, relocation, remote mode | User-declared preferences; location can still be a proxy |
| Desired salary, currency and employment type | Declared preference compatibility; salary is not a prediction |
| Job posting age | Freshness, with unknown dates neutral |
| Prior viewed/save/apply/explicit feedback | Bounded interest adjustment after sufficient history |
| Names, email, phone, account IDs | Excluded from feature matrix and candidate ranking text |
| Raw resume text | Excluded from ranking; only reviewed professional fields used |
| Gender, caste, religion, marital status, date of birth, nationality | No structured ranking feature; explicit sensitive lines removed from text |
| Employer rejection | Neutral outcome, not a negative preference signal |

The feature contract allowlists 13 professional numeric columns. Relevance labels
and protected/identity fields are not accepted as candidate feature inputs in the
evaluation dataset. Tests verify identity changes do not alter candidate text.

## Limitations and mitigations

Free-text professional fields may still contain demographic/organization proxies.
English dictionary extraction may favor familiar skill wording. Education, location,
salary preferences and behavior can correlate with socioeconomic background.
Pretrained embeddings can inherit biases; title-family priors and synthetic labels
can overvalue conventional career paths. Missing user skills may mean extraction
failure rather than lack of capability. Neutral unknown fits and editable review
fields reduce some of these problems but do not eliminate them.

No subgroup fairness metrics are claimed: the synthetic fixture has no appropriate
consented demographic evaluation population. Future work should use independently
reviewed judgments, documented lawful/consented audit attributes kept separate
from ranking features, subgroup retrieval metrics, counterfactual feature tests,
exposure auditing, error review and user feedback/reset/retention controls. Preserve
the visible baseline and bounded behavior weights to make changes reviewable.
