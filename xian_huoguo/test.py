
import json
import pandas

f = open("G:\\林老师问题\\name.json", encoding='utf-8')
data = json.load(f)

df = pandas.DataFrame()

enrollments = data["enrollments"]
for enrollment in enrollments:
    user = enrollment["user"]
    userNo = user["user_no"]
    name = user["name"]
    department = user["department"]["name"]
    email = user["email"]
    result = {
        'userNo': userNo,
        'name': name,
        'department': department,
        'email': email
    }
    print(result)
    df = df.append(result, ignore_index=True)
pandas.DataFrame(df).to_excel("G:\\林老师问题\\result.xlsx", sheet_name="result", index=False, header=True)



