# JobMatch viva notes · simple English + Hinglish

1. **What problem does the project solve?** It ranks jobs using a candidate's
   reviewed professional skills/preferences and explains gaps. Matlab suitable
   jobs ko order mein dikhata hai aur reason batata hai; placement guarantee nahi.
2. **Which parts are rule-based?** Skill overlap, experience/education/location/
   salary fit, quality checklist, learning dependencies and hybrid weights.
3. **What is TF-IDF?** A word representation that increases the importance of
   informative words in a catalogue. Cosine measures lexical similarity, not
   complete language understanding.
4. **What is a semantic embedding?** A pretrained neural encoder maps text to a
   numeric vector. Similar meanings may be close even without identical words.
   JobMatch's optional MiniLM module is implemented; weights were unavailable in
   this validation environment. Humne model ko scratch se train nahi kiya.
5. **What is trained here?** Logistic Regression on ordinal labels and Random
   Forest regression are experimental pointwise learning-to-rank baselines.
6. **Is the match score a probability?** No. It is a bounded compatibility/ranking
   utility. 85/100 does not mean an 85% chance of getting a job.
7. **Where do labels come from?** The committed 240 judgments are explicitly
   fictional author-created scenarios. Independent real review is still needed.
   Labels prediction formula se banaye nahi gaye.
8. **How do you prevent leakage?** Disjoint candidate groups, training-only
   vocabulary/IDF fitting, label-free features and temporal cutoffs for history.
9. **What does Precision@5 mean?** Relevant jobs in the top five divided by five.
   Relevant means label 2 or 3; weak label 1 contributes only to graded NDCG.
10. **Recall / NDCG / MRR / MAP?** Recall finds the fraction of all relevant jobs;
    NDCG rewards strong matches near the top; MRR rewards the first relevant job;
    MAP averages precision at relevant positions.
11. **What happens without embeddings or a model?** TF-IDF/hybrid still work.
    Missing/corrupt/incompatible rankers cannot crash the recommendation request.
12. **How is personalization controlled?** Five distinct jobs and three meaningful
    action jobs are required; behavior receives at most 10% of the weight.
13. **Does Resume Strength mean ATS compatibility?** No. It is a transparent,
    configurable evidence checklist. Confidence values are heuristic review aids.
14. **How are skill gaps and career paths calculated?** Exact/proficient skills
    receive full credit, beginner/related skills half, and missing skills zero.
    Prerequisites appear first; readiness is skill coverage, not promotion odds.
15. **How are models stored safely?** Validated JSON coefficients/trees, exact
    feature/dependency metadata and a digest. No arbitrary pickle/model uploads.
16. **Can you claim real-world accuracy or fairness?** No. Three held-out fictional
    candidates are too few; collect independent real judgments and audit subgroup
    retrieval/exposure errors before making broader claims.
