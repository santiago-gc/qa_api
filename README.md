# Airalo Automated API Requests

The file `test_api.py` has the following tests:

1. `test_get_token`: Test to get an OAuth2 token from the Airalo API.
2. `test_submit_order`: Test to verify an eSIM order submision based on quantity and package_id after getting a valid OAuth2 token.
3. `test_get_esims`: Test to retrieve a list of eSIMs and validate them after getting a valid OAuth2 token.

---
## Setup and Execution Instructions:


## 1. Create Project Directory

First, create a directory to house both the project repository and its virtual environment. A descriptive name like `airalo_api_test` is recommended.

```bash
mkdir airalo_api_test
cd airalo_api_test
```

## 2. Clone the Repository

Next, navigate into the directory you just created (`airalo_api_test`) and clone the project repository from GitHub.

```bash
git clone -b master https://github.com/santiago-gc/qa_api.git
```

## 3. Set Up the Virtual Environment

Inside the `airalo_api_test` directory, create and activate a Python virtual environment.

Linux:
```bash
python -m venv v_airalo
source v_airalo/bin/activate
```

Windows:
```bash
python -m venv v_airalo
v_airalo\Scripts\activate
```

## 4.  Install Dependencies

Once the virtual environment is created and activated, install the requirements from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

## 5. Configure Environment Variables

Create a `.env` file (in `qa_api`) to securely store The API credentials.

```
CLIENT_ID = "<your_ClientID>"
CLIENT_SECRET = "<your_ClientSecret>"
```

## 6. Verify the Directory Structure

The structure of `airalo_api_test` should look like this:

```
airalo_api_test/
├── v_airalo
└── qa_api/
    ├── .env
    ├── .gitignore
    ├── airalo_client.py
    ├── README.md
    ├── requirements.txt
    └── test_api.py
```

## 7. Run Tests

Switch to the directory `qa_api` and to execute the tests, you can simply run the command `pytest`.
