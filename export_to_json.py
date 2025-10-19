import sqlite3
import json

# Connect to your database
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Fetch all student data
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

# Convert each record into a dictionary (object)
students = []
for row in rows:
    students.append({
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "course": row[3]
    })

# Export to JSON file
with open('students_data.json', 'w', encoding='utf-8') as f:
    json.dump(students, f, indent=4, ensure_ascii=False)

conn.close()
print("✅ Data exported successfully to 'students_data.json'")
