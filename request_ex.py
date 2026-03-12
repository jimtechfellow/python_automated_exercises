import csv
import requests
# this version is better than GPT regarding production enviroment
URL = "https://jsonplaceholder.typicode.com/users"
OUT_CSV = "users.csv"
FIELDS = ["id", "name", "email", "company_name"]


def fetch_users(url: str) -> list:
    print(f"Fetching users from {url} ...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    if not isinstance(data, list):
        raise ValueError("Unexpected response format: expected a JSON list.")
    return data


def extract_rows(users: list) -> tuple[list, int]:
    print("Extracting fields ...")
    rows = []
    skipped = 0

    for i, user in enumerate(users, start=1):
        try:
            rows.append(
                {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"],
                    "company_name": user["company"]["name"],
                }
            )
        except (TypeError, KeyError):
            skipped += 1
            print(f"Warning: user record #{i} is missing expected fields. Skipping.")
    return rows, skipped


def write_csv(path: str, rows: list) -> None:
    print(f"Writing {len(rows)} rows to {path} ...")
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    try:
        users = fetch_users(URL)
        print(f"Received {len(users)} users.")
        rows, skipped = extract_rows(users)
        write_csv(OUT_CSV, rows)
        print("Done." + (f" Skipped {skipped} record(s)." if skipped else ""))
        return 0
    except requests.RequestException as exc:
        print(f"Request failed: {exc}")
        return 1
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}")
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}")
        raise


if __name__ == "__main__":
    raise SystemExit(main())