import sqlite3
import streamlit as st

# Database connection function
def get_connection():
    conn = sqlite3.connect("students.db")  # SQLite database file
    return conn

# Function to create table if not exists
def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER
        )
    ''')
    conn.commit()
    conn.close()

# Function to insert a new student
def insert_student(name, age):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO students (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()
    st.success("✅ Student added successfully!")

# Function to fetch students
def read_students():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()
    conn.close()
    return students

# Function to update student data
def update_student(student_id, name, age):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE students SET name = ?, age = ? WHERE id = ?", (name, age, student_id))
    conn.commit()
    conn.close()
    st.success("✅ Student updated successfully!")

# Function to delete student
def delete_student(student_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    st.success("✅ Student deleted successfully!")

# Create table at startup
create_table()

# Streamlit UI
st.title("🎓 Student Management System (SQLite)")

# Tabs for CRUD operations
tab1, tab2, tab3, tab4 = st.tabs(["➕ Create", "📋 Read", "✏️ Update", "🗑 Delete"])

with tab1:
    st.subheader("➕ Add a new student")
    with st.form("create_form"):
        name = st.text_input("Enter student's name")
        age = st.number_input("Enter student's age", min_value=1, max_value=100, step=1)
        submitted = st.form_submit_button("Add Student")
        if submitted:
            if name.strip():
                insert_student(name, age)
            else:
                st.warning("⚠ Please enter a valid name.")

with tab2:
    st.subheader("📋 View Students")
    students = read_students()
    if students:
        st.dataframe(students)  # Display data in a table
    else:
        st.info("No students found.")

with tab3:
    st.subheader("✏️ Update Student Details")
    students = read_students()
    if students:
        student_options = {f"{s[0]} - {s[1]}": s[0] for s in students}
        selected_student = st.selectbox("Select Student to Update", list(student_options.keys()))

        if selected_student:
            student_id = student_options[selected_student]
            new_name = st.text_input("Enter new name")
            new_age = st.number_input("Enter new age", min_value=1, max_value=100, step=1)
            if st.button("Update Student"):
                if new_name.strip():
                    update_student(student_id, new_name, new_age)
                else:
                    st.warning("⚠ Name cannot be empty.")

with tab4:
    st.subheader("🗑 Delete a Student")
    students = read_students()
    if students:
        student_options = {f"{s[0]} - {s[1]}": s[0] for s in students}
        selected_student = st.selectbox("Select Student to Delete", list(student_options.keys()))
        
        if st.button("Delete Student"):
            student_id = student_options[selected_student]
            delete_student(student_id)
    else:
        st.info("No students found.")
