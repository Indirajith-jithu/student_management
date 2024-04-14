<<<<<<< HEAD
# student_management
=======
# FastAPI Student Management API

This is a simple CRUD API built using FastAPI for managing student records.

## Features

- Create, read, update, and delete student records.
- Filter students by department and gender.
- PostgreSQL database backend.
- Streamlit app for user-friendly interaction.

## Installation

1. Clone the repository:

    ```
    git clone https://github.com/Indirajith-jithu/student_management.git
    cd student_management
    ```

2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

3. Set up the PostgreSQL database:
   
   - Make sure PostgreSQL is installed and running on your system.
   - Create a new database and update the connection string (SQLALCHEMY_DATABASE_URL) in `main.py`.

4. Run the FastAPI server:

    ```
    python main.py
    ```

5. Access the API at `http://localhost:8000` and API DOC at `http://localhost:8000/docs`.



## Usage

- Use the provided Streamlit app for a user-friendly interface to interact with the API.
- Use API endpoints directly for programmatic access.

## API Endpoints

- `POST /students/`: Create a new student record.
- `GET /students/`: Get all student records.
- `GET /students/{student_id}`: Get a specific student record.
- `PUT /students/{student_id}`: Update a student record.
- `DELETE /students/{student_id}`: Delete a student record.

## Streamlit App

To run the Streamlit app:

1. Install Streamlit if you haven't already:

    ```
    pip install streamlit
    ```

2. Run the app:

    ```
    streamlit run frontend.py
    ```

3. Access the app at `http://localhost:8501`.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
>>>>>>> master
