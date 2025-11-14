# SFTP File Handling Django Project

This project is a Django application that provides APIs for uploading and downloading files to an SFTP server, with file metadata stored in a PostgreSQL database.

## Setup Instructions

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Credentials:**
    -   Create a `.env` file in the `sftp_project` directory.
    -   Add the following content to the `.env` file, replacing the placeholder values with your SFTP and PostgreSQL server details:
        ```env
        # SFTP Configuration
        SFTP_HOST=your_sftp_host
        SFTP_PORT=22
        SFTP_USERNAME=your_sftp_username
        SFTP_PASSWORD=your_sftp_password

        # Database Configuration
        DB_NAME=your_db_name
        DB_USER=your_db_user
        DB_PASSWORD=your_db_password
        DB_HOST=localhost
        DB_PORT=5432
        ```

## Running the Project

1.  **Apply database migrations:**
    ```bash
    cd sftp_project
    python manage.py migrate
    ```

2.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be running at `http://127.0.0.1:8000/`.

## Testing the Project

1.  **Run the tests:**
    ```bash
    cd sftp_project
    python manage.py test sftp_files
    ```

## API Endpoints

-   **Upload a file:**
    -   **URL:** `/sftp/upload/`
    -   **Method:** `POST`
    -   **Form Data:** `file` (the file to upload)
    -   **Success Response:**
        ```json
        {
            "message": "File uploaded successfully",
            "file_id": 1
        }
        ```

-   **Download a file:**
    -   **URL:** `/sftp/download/<file_id>/`
    -   **Method:** `GET`
