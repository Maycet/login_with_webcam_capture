# login_with_webcam_capture
Academic prototype for a login app with camera authentication.

## Description
This project is an academic prototype for a login application that uses camera authentication. It captures images from the webcam and uses OpenCV for facial recognition.

## Installation
To run this project, you need to have Python and the required libraries installed. Follow the steps below to set up the project:

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/login_with_webcam_capture.git
    cd login_with_webcam_capture
    ```

2. Install the required libraries:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
The `hackathon.pyw` file is the main script to execute the application. Run the script using the following command:
```bash
python hackathon.pyw
```

## Performance
The camera component may have a slight delay during the initial loading time due to the initialization of the OpenCV classes and webcam access. Optimizations are welcome to improve performance.

## Data
The `data.json` file is used as a test database for the registered users.
