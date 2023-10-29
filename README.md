# Baseball Stats Application README

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Run the Application](#run-the-application)
- [Stop the Application](#stop-the-application)

## Description

This is a Flask-based Python application for the Atlanta Braves Developer Exercise. 
The solution for MousePos.html is located in this project in a file called MousePos_CORRECTED.html.

## Dependencies

The application relies on the following Python libraries and frameworks:

- Flask
- pandas
- plotly
- openpyxl

## Installation

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/jonesmiasia/AtlantaBravesDeveloperExercises.git
   ```
2. Navigate to the project directory:
    ```
    cd AtlantaBravesDeveloperExercises
    ```
3. Create a virtual environment (recommended):
    ```
    python -m venv .venv
    ```

4. Activate the virtual environment:
    - On Windows:

        ```
        .venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```
        source .venv/bin/activate
        ```

5. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```



## Run the Application

1. Make sure your virtual environment is activated.
2. Run the Flask application in:

    ```
    flask run
    ```
3. Access the application in your web browser at [http://localhost:5000](http://localhost:5000) or another URL specified in the terminal.

## Stop the Application
Press `CTRL + C` in the terminal to stop the application.
