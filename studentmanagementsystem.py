import streamlit as st
import pymysql

# Database connection function
def get_connection():
    try:
        conn = pymysql.connect(
            host='your-remote-host',  # e.g., 'db4free.net' or 'your-server-ip'
            user='your-username',
            password='your-password',
            database='your-database',
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        st.error(f"❌ Database Connection Error: {e}")
        return None

# Function to create table if not exists
def create_table():
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    age INT
                )
            ''')
            conn.commit()
        except Exception as e:
            st.error(f"❌ Error creating table: {e}")
        finally:
            conn.close()

# Function to insert a new student
def insert_student(name, age):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO students (name, age) VALUES (%s, %s)", (name, age))
            conn.commit()
            st.success("✅ Student added successfully!")
        except Exception as e:
            st.error(f"❌ Error inserting student: {e}")
        finally:
            conn.close()

# Function to fetch students
def read_students():
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM students")
            students = cur.fetchall()
            return students
        except Exception as e:
            st.error(f"❌ Error fetching students: {e}")
            return []
        finally:
            conn.close()
    return []

# Function to update student data
def update_student(student_id, name, age):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("UPDATE students SET name = %s, age = %s WHERE id = %s", (name, age, student_id))
            conn.commit()
            st.success("✅ Student updated successfully!")
        except Exception as e:
            st.error(f"❌ Error updating student: {e}")
        finally:
            conn.close()

# Function to delete student
def delete_student(student_id):
    conn = get_connection()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM students WHERE id = %s", (student_id,))
            conn.commit()
            st.success("✅ Student deleted successfully!")
        except Exception as e:
            st.error(f"❌ Error deleting student: {e}")
        finally:
            conn.close()

# Create table at startup
create_table()

# Streamlit UI
st.title("🎓 Student Management System")

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
        student_options = {f"{s['id']} - {s['name']}": s['id'] for s in students}
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
        student_options = {f"{s['id']} - {s['name']}": s['id'] for s in students}
        selected_student = st.selectbox("Select Student to Delete", list(student_options.keys()))
        
        if st.button("Delete Student"):
            student_id = student_options[selected_student]
            delete_student(student_id)
    else:
        st.info("No students found.")
