# Computational checks for neutrosophic probability logics

Reproducibility package for *Complete probability logics for neutrosophic
triples: a response to Rivieccio's completeness question*, associated with
Florentin Smarandache and Maikel Yelandi Leyva-Vázquez, in that order.
Package version: **1.0.0**.

The package runs eleven computational sanity checks for the paper's
computational appendix (Appendix A in the original source, numbered
Section 12 in the Word export). It contains the original numerical script,
archived reference results, and a runner that checks the results instead of
relying on the numerical script's exit status alone.

## Reproduce

The numerical reference run was reproduced with **Python 3.14.3**,
**NumPy 2.4.4**, and **SciPy 1.17.1** on Windows. The two library versions
are pinned in `requirements.txt`. Other Python/library versions and operating
systems have not been validated for this release.

Windows PowerShell, from the repository root:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe scripts/run_checks.py
```

POSIX shells, from the repository root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python scripts/run_checks.py
```

The numerical run uses Python's `random` and NumPy's random generator,
both seeded with **20261001**. Expect several minutes for the linear
programming checks. Package installation requires access to a package index;
the checks themselves do not access the network or require datasets,
credentials, API keys, or external services.

The runner creates `results/`, runs the unchanged original script, records
the interpreter/library versions in `results/environment.json`, and calls
the verifier. It exits unsuccessfully if the numerical script fails,
reference results differ, or mismatch/violation/certificate-error counters
are nonzero. Each run overwrites `results/`; `reference_results/` is preserved.
The historical script alone does not make every printed failed check fatal.

To verify an already generated results file:

```sh
python scripts/verify_results.py
```

The verifier requires the full hierarchy of eleven reference checks,
compares integer counts, booleans and strings exactly, and compares finite
floating-point values with absolute and relative tolerances of **1e-9**.
Tolerances apply to reproduction of recorded numerical outputs, not to a
claim that a formal proof has been machine verified.

## Checks

| Check | What is tested | Reference sample |
| --- | --- | --- |
| 1 | Translation between neutrosophic and upper-probability expressions | 4,000 formulas |
| 2 | Validities of the normalized coherent fragment and an explicit failure of subadditivity of indeterminacy | 3,000 random cases |
| 3 | Two separating examples for weak normalized versus coherent semantics | C1 and C2 |
| 4 | Lower-cover/Farkas certificate and envelope computations on restricted event domains | 600 cases; 12,000 soundness instances |
| 5 | Faithful regions of the minimal, Belnap and disjoint liftings | 3,000 points |
| 6 | Lifted validities and tightness of the truth conjunction bound | 1,500 random cases; 300 Fréchet tightness trials |
| 7 | Truth preservation compared with LP, FDE and K3 | 14,400 formula pairs |
| 8 | Satisfiability reduction on generated Boolean CNFs | 150 CNFs |
| 9 | Indeterminacy-sensitive consequence on the minimal lifting | 14,400 formula pairs |
| 10 | Matching truth/falsity with different indeterminacy | 500 formulas |
| 11 | Real signed-charge representations and exact-cover certificates | 2,000 triples and 400 domain cases |

The original log order is 1, 2, 3, 5, 4, 6, 7, 8, 10, 9, 11.
Successful reproduction finds no recorded violation or mismatch, and no bad
certificate, with the original seed and finite samples. Reference maximum
errors in representation/envelope computations are below **1e-15**.

## Scope and limitations

These computations confirm worked examples and search finite/random cases
for counterexamples. They do **not** prove soundness, completeness,
NP-completeness, strong completeness, or a truth-functional neutrosophic
calculus. They do not independently validate the added historical discussion
of Imamura and Smarandache, validate every bibliographic reference, or certify
every possible semantic frame. Formal theorems still depend on their proofs.

The script's references to companion-paper theorem numbers are historical
labels from the original supplement. The package contains no manuscript.

## Files

- `scripts/completeness_checks.py`: original mathematical computations.
- `scripts/run_checks.py`: creates output directories and runs verification.
- `scripts/verify_results.py`: fails on meaningful result discrepancies.
- `reference_results/`: immutable archived JSON and human-readable log.
- `results/`: fresh numerical JSON, log and tested environment.
- `requirements.txt`: pinned numerical dependencies.
- `CITATION.cff`: software citation, with research-author order supplied for this artifact.
- `.zenodo.json`: prepared deposition metadata; no DOI or repository URL assigned.
- `source_manifest.json`, `PROVENANCE.md`, `LICENSE`, `licenses/UPSTREAM_MIT.txt`: source integrity and inherited notices.

## Citation and licensing

Use `CITATION.cff` to cite this computational artifact. Its contributor order
follows the associated research article; it does not assert who originally
programmed each file. Update citation identifiers after the public release
receives its DOI. No identifier is reserved or fabricated in this package.

The supplementary material explicitly carried **CC BY 4.0**. The parent
project also carried an MIT notice; that original notice is retained in full.
See `PROVENANCE.md` and `LICENSE` for the inherited notice scopes.
