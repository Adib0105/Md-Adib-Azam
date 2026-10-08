# Experiments and feedback

Experiments are **disabled by default**. The operator must create metadata first:

```bash
python scripts/manage_experiment.py weighted-versus-hybrid-v1 --enable
```

Set `ML_EXPERIMENT=weighted-versus-hybrid-v1` and restart. Candidates are assigned
deterministically by secret-key HMAC of experiment version/user ID. Assignment A
uses the seven-factor baseline; B uses hybrid. The assignment, selected strategy,
model version and time are stored before displayed recommendations are exposed.
Do not change the models/version of an already enrolled experiment; create a new
slug for a new comparison. Candidate cards/details disclose recorded assignment.
Admins are not enrolled. Stopping an experiment retains the historical records.

Exposure records contain the returned page's jobs, positions, scores, actual model
version and request ID. Simulation results and undisplayed rankings are not logged
as recommendation exposures. Job-detail views, saves, local tracker applies,
explicit ignore/reject and interview/offer updates become immutable feedback.
No application is sent to an employer by the local tracker.

The ML Lab attributes viewed/saved/applied actions to the most recent exposure of
the same user/job within seven days. Counts are exploratory event counts, not
unique-user conversion rates or a statistical significance test. Repeated actions
and exposure bias remain possible. Lack of an action is never invented as an
`ignored` event. Training does not automatically relabel these logs as relevance.
No real behavioral evaluation has been run for this release.

Offline training/evaluation reports include dataset hash, split methodology,
dependencies, feature/model versions, parameters and held-out metrics. Evaluated
models can be written with `--artifacts instance/ml/evaluation-models`. Separate
operator instances/output directories prevent overwriting experiments. This is
lightweight file/metadata tracking, not a full MLflow deployment.
