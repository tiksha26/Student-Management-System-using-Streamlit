
import streamlit as st
import sqlite3
import pandas as pd

# Connect to database (creates student.db automatically)
conn = sqlite3.connect("student.db", check_same_thread=False)
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll INTEGER PRIMARY KEY,
    name TEXT,
    age INTEGER,
    course TEXT,
    marks REAL
)
""")
conn.commit()

st.title("Student Record Management System")

menu = st.sidebar.selectbox(
    "Choose Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.subheader("Add Student")

    roll = st.number_input("Roll Number", min_value=1, step=1)
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1, step=1)
    course = st.text_input("Course")
    marks = st.number_input("Marks", min_value=0.0, max_value=100.0)

    if st.button("Add"):
        try:
            cursor.execute(
                "INSERT INTO students VALUES (?, ?, ?, ?, ?)",
                (roll, name, age, course, marks)
            )
            conn.commit()
            st.success("Student Added Successfully!")
        except sqlite3.IntegrityError:
            st.error("Roll Number already exists!")

# READ
elif menu == "View Students":
    st.subheader("Student Records")

    df = pd.read_sql_query("SELECT * FROM students", conn)
    st.dataframe(df, use_container_width=True)

# UPDATE
elif menu == "Update Student":
    st.subheader("Update Student")

    cursor.execute("SELECT roll FROM students")
    rolls = [row[0] for row in cursor.fetchall()]

    if rolls:
        roll = st.selectbox("Select Roll Number", rolls)

        cursor.execute("SELECT * FROM students WHERE roll=?", (roll,))
        student = cursor.fetchone()

        name = st.text_input("Name", student[1])
        age = st.number_input("Age", min_value=1, value=student[2])
        course = st.text_input("Course", student[3])
        marks = st.number_input("Marks", min_value=0.0, max_value=100.0,
                                value=float(student[4]))

        if st.button("Update"):
            cursor.execute("""
                UPDATE students
                SET name=?, age=?, course=?, marks=?
                WHERE roll=?
            """, (name, age, course, marks, roll))

            conn.commit()
            st.success("Student Updated Successfully!")
    else:
        st.info("No student records found.")

# DELETE
elif menu == "Delete Student":
    st.subheader("Delete Student")

    cursor.execute("SELECT roll FROM students")
    rolls = [row[0] for row in cursor.fetchall()]

    if rolls:
        roll = st.selectbox("Select Roll Number", rolls)

        if st.button("Delete"):
            cursor.execute("DELETE FROM students WHERE roll=?", (roll,))
            conn.commit()
            st.success("Student Deleted Successfully!")
    else:
        st.info("No student records found.")

conn.close()
