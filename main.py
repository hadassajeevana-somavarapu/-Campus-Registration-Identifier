# Campus Registration Identifier Analyzer
# Validates campus registration IDs (format: YY-BBB-SSSS), extracts admission year,
# branch code, and serial number, and classifies records by branch and admission year.

BRANCH_MAP = {
    "CSE": "Computer Science and Engineering",
    "ECE": "Electronics and Communication Engineering",
    "EEE": "Electrical and Electronics Engineering",
    "MEC": "Mechanical Engineering",
    "CIV": "Civil Engineering",
    "AID": "Artificial Intelligence and Data Science",
}

MIN_ADMISSION_YEAR = 2000
MAX_ADMISSION_YEAR = 2026


def parse_and_validate_id(reg_id):
    """
    Validates format YY-BBB-SSSS and returns a dictionary of extracted components.
    Raises ValueError with a clear reason if invalid.
    """
    if not isinstance(reg_id, str):
        raise ValueError("Registration ID must be a string.")

    cleaned = reg_id.strip().upper()
    parts = cleaned.split("-")

    if len(parts) != 3:
        raise ValueError("Invalid structure. Expected format YY-BBB-SSSS (e.g., 24-CSE-0105).")

    year_code, branch_code, serial_str = parts

    # Validate 2-digit admission year
    if not (len(year_code) == 2 and year_code.isdigit()):
        raise ValueError(f"Invalid admission year code '{year_code}'. Must be 2 digits.")

    admission_year = 2000 + int(year_code)
    if not (MIN_ADMISSION_YEAR <= admission_year <= MAX_ADMISSION_YEAR):
        raise ValueError(
            f"Admission year {admission_year} is outside valid range ({MIN_ADMISSION_YEAR}-{MAX_ADMISSION_YEAR})."
        )

    # Validate 3-letter branch code
    if not (len(branch_code) == 3 and branch_code.isalpha()):
        raise ValueError(f"Invalid branch code '{branch_code}'. Must be 3 alphabetic letters.")

    if branch_code not in BRANCH_MAP:
        raise ValueError(f"Unrecognized branch code '{branch_code}'.")

    # Validate 4-digit serial number (cannot be 0000)
    if not (len(serial_str) == 4 and serial_str.isdigit()):
        raise ValueError(f"Invalid serial number '{serial_str}'. Must be 4 digits.")

    serial_num = int(serial_str)
    if serial_num == 0:
        raise ValueError("Serial number cannot be '0000'.")

    return {
        "raw_id": reg_id.strip(),
        "normalized_id": cleaned,
        "year_code": year_code,
        "admission_year": admission_year,
        "branch_code": branch_code,
        "branch_name": BRANCH_MAP[branch_code],
        "serial_str": serial_str,
        "serial_num": serial_num,
    }


def analyze_records(reg_ids):
    """
    Processes a list of registration IDs, separating valid and invalid records
    and grouping valid records by branch and by admission year.
    """
    valid_records = []
    invalid_records = []
    by_branch = {}
    by_year = {}

    for raw_id in reg_ids:
        try:
            info = parse_and_validate_id(raw_id)
            valid_records.append(info)

            b_key = f"{info['branch_code']} ({info['branch_name']})"
            by_branch.setdefault(b_key, []).append(info["normalized_id"])

            y_key = str(info["admission_year"])
            by_year.setdefault(y_key, []).append(info["normalized_id"])
        except ValueError as err:
            invalid_records.append({
                "raw_id": raw_id.strip(),
                "reason": str(err),
            })

    return {
        "valid_records": valid_records,
        "invalid_records": invalid_records,
        "by_branch": by_branch,
        "by_year": by_year,
    }


def print_analysis_report(result):
    print("\n" + "=" * 76)
    print("CAMPUS REGISTRATION IDENTIFIER ANALYSIS REPORT")
    print("=" * 76)

    print(f"\nValid Records ({len(result['valid_records'])}):")
    if result["valid_records"]:
        for rec in result["valid_records"]:
            print(
                f"  * {rec['normalized_id']:<12} | Year: {rec['admission_year']} | "
                f"Branch: {rec['branch_code']} ({rec['branch_name']}) | Serial: {rec['serial_num']}"
            )
    else:
        print("  None")

    print(f"\nInvalid Records ({len(result['invalid_records'])}):")
    if result["invalid_records"]:
        for bad in result["invalid_records"]:
            print(f"  * '{bad['raw_id']}' -> {bad['reason']}")
    else:
        print("  None")

    print("\n--- Classification by Branch ---")
    for branch_label, ids in sorted(result["by_branch"].items()):
        print(f"  * {branch_label} [{len(ids)}]: {', '.join(ids)}")

    print("\n--- Classification by Admission Year ---")
    for year_label, ids in sorted(result["by_year"].items()):
        print(f"  * Batch {year_label} [{len(ids)}]: {', '.join(ids)}")

    print("=" * 76)


def main():
    print("Expected ID Format: YY-BBB-SSSS (e.g., 24-CSE-0105)")
    print("Supported Branches:", ", ".join(f"{k}={v}" for k, v in BRANCH_MAP.items()))

    count = int(input("\nHow many registration IDs do you want to analyze? "))
    reg_ids = []
    for i in range(1, count + 1):
        reg_id = input(f"  Enter Registration ID #{i}: ")
        reg_ids.append(reg_id)

    result = analyze_records(reg_ids)
    print_analysis_report(result)


if __name__ == "__main__":
    main()
