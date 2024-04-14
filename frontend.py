import requests
import streamlit as st
import pandas as pd

# FastAPI base URL
BASE_URL = "http://localhost:8000"

# Function to retrieve students with optional filters
def get_students(filters=None):
    url = f"{BASE_URL}/students/"
    if filters:
        url += "?" + "&".join(f"{k}={v}" for k, v in filters.items())
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error: {response.status_code}")

# Function to create a new student
def create_student(name, age, gender, department):
    data = {
        "name": name,
        "age": age,
        "gender": gender,
        "department": department
    }
    response = requests.post(f"{BASE_URL}/students/", json=data)
    if response.status_code == 200:
        st.success("Student created successfully")
    else:
        st.error(f"Error: {response.status_code}")

# Function to delete a student
def delete_student(student_id):
    response = requests.delete(f"{BASE_URL}/students/{student_id}")
    if response.status_code == 200:
        st.success("Student deleted successfully")
    else:
        st.error(f"Error: {response.status_code}")

# Streamlit UI
st.title("Student Management")
st.markdown("---")

# Define tabs
tabs = ["Create Student", "View Students", "Delete Student"]
selected_tab = st.sidebar.radio("Select Action", tabs)

# Create student tab
if selected_tab == "Create Student":
    st.subheader("Create Student")
    with st.form("create_student_form"):
        new_name = st.text_input("Name")
        new_age = st.number_input("Age", min_value=0, max_value=150)
        new_gender = st.selectbox("Gender", ["male", "female"])
        new_department = st.selectbox("Department", ["Computer Science", "Mathematics", "Physics", "Biology", "History"])
        submitted = st.form_submit_button("Create")
        if submitted:
            create_student(new_name, new_age, new_gender, new_department)
            st.success("Student created successfully")

# View students tab
elif selected_tab == "View Students":
    st.subheader("View Students")
    # Filter options
    st.sidebar.subheader("Filters")
    selected_department = st.sidebar.multiselect("Department", ["All", "Computer Science", "Mathematics", "Physics", "Biology", "History"],default='All')
    selected_gender = st.sidebar.multiselect("Gender", ["All", "male", "female"],default='All')

    # Prepare filters
    filters = {}
    if "All" not in selected_department:
        filters["department"] = selected_department
    if "All" not in selected_gender :
        filters["gender"] = selected_gender

    # Retrieve students with filters
    students = get_students(filters)

    df = pd.DataFrame(students)
    if filters:
        for key, value in filters.items():
            df = df[df[key].isin(value) ]
    # Display students
    if students:
        # Create pandas DataFrame
        st.dataframe(df)
    else:
        st.info("No students found")

# Delete student tab
elif selected_tab == "Delete Student":
    st.subheader("Delete Student")
    delete_id = st.number_input("Student ID to delete", min_value=1, step=1)
    if st.button("Delete"):
        delete_student(delete_id)
