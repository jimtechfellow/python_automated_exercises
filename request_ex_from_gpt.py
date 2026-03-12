import csv
import requests
# This is from chatgpt exercises codes which is easy to understand.
url = "https://jsonplaceholder.typicode.com/users"
output_file = "users.csv"

try:
    print("开始请求 API...")
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    print(f"成功获取 {len(data)} 条记录")

    with open(output_file, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "name", "email", "company_name"])

        for user in data:
            writer.writerow([
                user["id"],
                user["name"],
                user["email"],
                user["company"]["name"]
            ])

    print(f"成功写入文件: {output_file}")

except requests.RequestException as e:
    print("请求失败:", e)

except KeyError as e:
    print("字段缺失:", e)

except Exception as e:
    print("未知错误:", e)