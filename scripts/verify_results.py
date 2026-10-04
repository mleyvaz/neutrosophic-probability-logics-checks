"""Compare all archived outputs and fail on nonzero error counters."""
from pathlib import Path
import argparse
import json
import math

ABS_TOL = 1e-9
REL_TOL = 1e-9
EXPECTED_CHECKS = {
    "check1_translation", "check2_validities", "check3_weak_vs_coherent",
    "check4_farkas_covers", "check5_faithful_regions", "check6_lifted_validities",
    "check7_consequence", "check8_reduction", "check9_I_sensitive_consequence",
    "check10_I_not_definable", "check11_signed",
}


def compare(reference, actual, path="results"):
    errors = []
    if isinstance(reference, dict):
        if not isinstance(actual, dict):
            return [f"{path}: expected object"]
        if set(reference) != set(actual):
            errors.append(f"{path}: keys differ")
        for key in sorted(set(reference) & set(actual)):
            errors.extend(compare(reference[key], actual[key], f"{path}.{key}"))
    elif isinstance(reference, list):
        if not isinstance(actual, list) or len(reference) != len(actual):
            return [f"{path}: list length/type differs"]
        for i, (expected, observed) in enumerate(zip(reference, actual)):
            errors.extend(compare(expected, observed, f"{path}[{i}]"))
    elif isinstance(reference, float):
        if isinstance(actual, bool) or not isinstance(actual, (int, float)):
            errors.append(f"{path}: expected finite number")
        elif not math.isfinite(actual) or not math.isclose(
            reference, actual, abs_tol=ABS_TOL, rel_tol=REL_TOL
        ):
            errors.append(f"{path}: {actual!r} differs from {reference!r}")
    elif type(reference) is not type(actual) or reference != actual:
        errors.append(f"{path}: {actual!r} differs from {reference!r}")
    return errors


def counter_errors(value, path="results", inside_counter=False):
    errors = []
    if isinstance(value, dict):
        for key, child in value.items():
            counter = inside_counter or key in {"violations", "mismatches"} or key in {
                "certificates_bad", "sound_violations", "TF_disagreements"
            }
            errors.extend(counter_errors(child, f"{path}.{key}", counter))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            errors.extend(counter_errors(child, f"{path}[{i}]", inside_counter))
    elif inside_counter and (isinstance(value, bool) or not isinstance(value, int) or value != 0):
        errors.append(f"{path}: error counter must be integer zero, got {value!r}")
    return errors


def main():
    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--actual", type=Path, default=root / "results/completeness_checks.json")
    parser.add_argument("--reference", type=Path, default=root / "reference_results/completeness_checks.json")
    args = parser.parse_args()
    reference = json.loads(args.reference.read_text(encoding="utf-8"))
    actual = json.loads(args.actual.read_text(encoding="utf-8"))
    errors = []
    if not isinstance(reference, dict) or set(reference) != EXPECTED_CHECKS:
        errors.append("Reference must contain exactly the eleven documented checks.")
    if not isinstance(actual, dict) or set(actual) != EXPECTED_CHECKS:
        errors.append("Actual results must contain exactly the eleven documented checks.")
    errors.extend(compare(reference, actual))
    errors.extend(counter_errors(actual))
    if errors:
        for error in errors:
            print("FAIL:", error)
        return 1
    print("PASS: all eleven checks match reference results; error counters are zero.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
