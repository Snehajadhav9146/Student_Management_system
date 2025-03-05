import streamlit as st
import pymysql

# Connect to the database
conn = pymysql.connect(
    host='localhost',  # or '127.0.0.1'
    user='root',
    password='',
    database='shital'
)

# Create a cursor object
cur = conn.cursor()

# Confirm the connection
st.write("Database connected successfully!")

# Create a table
cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT
    )
''')

# Confirm table creation
st.write("Table created successfully!")

# Function to insert data from user input
def insert_student(name, age):
    cur.execute("INSERT INTO students (name, age) VALUES (%s, %s)", (name, age))
    conn.commit()
    st.write("Data inserted successfully!")

# Function to read data
def read_students():
    cur.execute("SELECT * FROM students")
    return cur.fetchall()

# Function to update data
def update_student(student_id, name, age):
    cur.execute("UPDATE students SET name = %s, age = %s WHERE id = %s", (name, age, student_id))
    conn.commit()
    st.write("Data updated successfully!")

# Function to delete data
def delete_student(student_id):
    cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
    conn.commit()
    st.write("Data deleted successfully!")

# Streamlit interface
st.header("Student Management System")

# Tabs for different CRUD operations
tab1, tab2, tab3, tab4 = st.tabs(["Create", "Read", "Update", "Delete"])

with tab1:
    st.subheader("Add a new student")
    with st.form("create_form"):
        name = st.text_input("Enter student's name")
        age = st.number_input("Enter student's age", min_value=0)
        submitted = st.form_submit_button("Submit")
        if submitted:
            insert_student(name, age)

with tab2:
    st.subheader("View students")
    students = read_students()
    for student in students:
        st.write(student)

with tab3:
    st.subheader("Update a student")
    with st.form("update_form"):
        student_id = st.number_input("Enter student's ID to update", min_value=0)
        name = st.text_input("Enter new name")
        age = st.number_input("Enter new age", min_value=0)
        submitted = st.form_submit_button("Update")
        if submitted:
            update_student(student_id, name, age)

with tab4:
    st.subheader("Delete a student")
    with st.form("delete_form"):
        student_id = st.number_input("Enter student's ID to delete", min_value=0)
        submitted = st.form_submit_button("Delete")
        if submitted:
            delete_student(student_id)

# Close the connection
conn.close()
st.write("Connection closed.")
