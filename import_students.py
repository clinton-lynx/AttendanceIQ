import openpyxl
import sqlite3
import os

# Path to your excel file and database
EXCEL_PATH = "FINAL CLASS LIST.xlsx"
DB_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "attendance.db")

def import_students():
    # Load the Excel file
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: {EXCEL_PATH} not found.")
        return

    wb = openpyxl.load_workbook(EXCEL_PATH)
    ws = wb.active

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    count = 0
    # Dummy encoding for initialization (128 zeros)
    dummy_encoding = bytes([0] * 128) 

    for row in ws.iter_rows(min_row=2, values_only=True):  # skip header row
        # Ensure row has at least 3 elements
        if len(row) < 3:
            continue
            
        sn, name, matric = row[0:3]

        if not name or not matric:  # skip empty rows
            continue

        name = name.strip()                    # remove extra spaces
        matric = str(int(matric)).strip()      # convert from float to clean string

        try:
            cursor.execute(
                "INSERT INTO students (student_id, name, face_encoding) VALUES (?, ?, ?)",
                (matric, name, dummy_encoding)
            )
            count += 1
        except sqlite3.IntegrityError:
            print(f"Skipping duplicate: {matric}")  # already exists

    conn.commit()
    conn.close()
    print(f"Successfully imported {count} students.")

if __name__ == "__main__":
    import_students()