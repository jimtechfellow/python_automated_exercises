import csv
import requests

USERS_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_CSV = "users.csv"


def fetch_users():
    """
    Fetch users from the API and return a minimal result dict.

    Result format:
    {
        "ok": bool,
        "stage": str,
        "reason": str,
        "evidence": any
    }
    """
    result = {
        "ok": False,
        "stage": "fetch_users",
        "reason": "",
        "evidence": None,
    }

    try:
        response = requests.get(USERS_URL, timeout=20)
        response.raise_for_status()
    except requests.RequestException as exc:
        result["reason"] = f"Request failed: {exc}"
        return result

    try:
        data = response.json()
    except ValueError as exc:
        result["reason"] = f"Failed to parse JSON: {exc}"
        return result

    if not isinstance(data, list):
        result["reason"] = "Unexpected response format (expected a list)."
        result["evidence"] = type(data).__name__
        return result

    result["ok"] = True
    result["reason"] = "Users fetched successfully."
    result["evidence"] = data
    return result


def save_users_to_csv(users):
    """
    Save users to a CSV file and return a minimal result dict.

    Only the required fields are written:
    id, name, email, phone, website, company_name
    """
    result = {
        "ok": False,
        "stage": "save_users_to_csv",
        "reason": "",
        "evidence": None,
    }

    rows = []
    skipped = 0

    for index, user in enumerate(users, start=1):
        try:
            row = {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "phone": user["phone"],
                "website": user["website"],
                "company_name": user["company"]["name"],
            }
            rows.append(row)
        except (KeyError, TypeError):
            skipped += 1

    try:
        with open(OUTPUT_CSV, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=[
                    "id",
                    "name",
                    "email",
                    "phone",
                    "website",
                    "company_name",
                ],
            )
            writer.writeheader()
            writer.writerows(rows)
    except OSError as exc:
        result["reason"] = f"Failed to write CSV: {exc}"
        result["evidence"] = {"rows_attempted": len(rows), "skipped": skipped}
        return result

    result["ok"] = True
    result["reason"] = "CSV written successfully."
    result["evidence"] = {
        "rows_written": len(rows),
        "skipped": skipped,
        "output_file": OUTPUT_CSV,
    }
    return result


def main():
    print("Starting user export...")

    fetch_result = fetch_users()
    print(
        f"[{fetch_result['stage']}] ok={fetch_result['ok']} "
        f"reason='{fetch_result['reason']}'"
    )

    if not fetch_result["ok"]:
        print("Stopping because fetching users failed.")
        return 1

    users = fetch_result["evidence"]
    print(f"Fetched {len(users)} users. Saving to CSV...")

    save_result = save_users_to_csv(users)
    print(
        f"[{save_result['stage']}] ok={save_result['ok']} "
        f"reason='{save_result['reason']}'"
    )

    if save_result["ok"]:
        evidence = save_result["evidence"]
        print(
            f"Done. Wrote {evidence['rows_written']} row(s) to "
            f"{evidence['output_file']}. Skipped {evidence['skipped']} record(s)."
        )
        return 0
    else:
        print("Saving users failed.")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())