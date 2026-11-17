
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Management System", page_icon="🎓")

st.title("🎓 Student Record Management System")
st.write("Manage student records using CRUD operations.")

# Initialize student data
if "students" not in st.session_state:
    st.session_state.students = pd.DataFrame(
        columns=["Roll No", "Name", "Age", "Course", "Marks"]
    )

# Menu
menu = st.sidebar.selectbox(
    "Select Operation",
    ["Add Student", "View Students", "Update Student", "Delete Student"]
)

# CREATE
if menu == "Add Student":
    st.subheader("Add New Student")

    with st.form("add_form"):
        roll = st.number_input("Roll Number", min_value=1, step=1)
        name = st.text_input("Student Name")
        age = st.number_input("Age", min_value=1, max_value=100)
        course = st.text_input("Course")
        marks = st.number_input("Marks", min_value=0, max_value=100)

        submit = st.form_submit_button("Add Student")

        if submit:
            if name.strip() == "" or course.strip() == "":
                st.error("Please enter all details.")
            elif roll in st.session_state.students["Roll No"].values:
                st.error("Roll Number already exists!")
            else:
                new_student = pd.DataFrame([{
                    "Roll No": roll,
                    "Name": name,
                    "Age": age,
                    "Course": course,
                    "Marks": marks
                }])

                st.session_state.students = pd.concat(
                    [st.session_state.students, new_student],
                    ignore_index=True
                )

                st.success("Student added successfully!")

# READ
elif menu == "View Students":
    st.subheader("All Student Records")

    if not st.session_state.students.empty:
        st.dataframe(st.session_state.students, use_container_width=True)
    else:
        st.info("No student records available.")

# UPDATE
elif menu == "Update Student":
    st.subheader("Update Student Details")

    df = st.session_state.students

    if not df.empty:
        roll = st.selectbox("Select Roll Number", df["Roll No"].tolist())

        student = df[df["Roll No"] == roll].iloc[0]

        with st.form("update_form"):
            name = st.text_input("Name", value=student["Name"])
            age = st.number_input("Age", min_value=1, max_value=100,
                                  value=int(student["Age"]))
            course = st.text_input("Course", value=student["Course"])
            marks = st.number_input("Marks", min_value=0, max_value=100,
                                    value=int(student["Marks"]))

            update = st.form_submit_button("Update Student")

            if update:
                idx = st.session_state.students[
                    st.session_state.students["Roll No"] == roll
                ].index[0]

                st.session_state.students.loc[idx, ["Name", "Age", "Course", "Marks"]] = [
                    name, age, course, marks
                ]

                st.success("Student record updated successfully!")
    else:
        st.info("No records available to update.")

# DELETE
elif menu == "Delete Student":
    st.subheader("Delete Student Record")

    df = st.session_state.students

    if not df.empty:
        roll = st.selectbox("Select Roll Number to Delete",
                            df["Roll No"].tolist())

        if st.button("Delete Student"):
            st.session_state.students = df[
                df["Roll No"] != roll
            ].reset_index(drop=True)

            st.success("Student record deleted successfully!")
    else:
        st.info("No records available to delete.")
