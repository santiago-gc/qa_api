# Airalo Automated API Requests

The file `test_api.py` has the following main tests:

1. `test_get_token`: Test to get an OAuth2 token from the Airalo API.
2. `test_submit_order_6eSIM`: Test to verify an eSIM order submision based on quantity (6 as indicated in the requirements) and package_id after getting a valid OAuth2 token.
3. `test_get_esims`: Test to retrieve a list of eSIMs and validate that they correspond to a previously submitted order after getting a valid OAuth2 token.

The other 4 tests verify boundary contditions when generating an eSIM order (2 are expected to fail for ordering an invalid amount of eSIMs).

---
## Setup and Execution Instructions:


## 1. Create Project Directory

First, create a directory to house both the project repository and its virtual environment. A descriptive name like `airalo_api_test` is recommended.

```bash
mkdir airalo_api_test
cd airalo_api_test
```

## 2. Clone the Repository

Next, navigate into the directory you just created (`airalo_api_test/`) and clone the project repository from GitHub.

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

Create a `.env` file (in `qa_api/`) to securely store The API credentials.

```
CLIENT_ID = "<your_ClientID>"
CLIENT_SECRET = "<your_ClientSecret>"
```

## 6. Verify the Directory Structure

The structure of `airalo_api_test/` should look like this:

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

Switch to the directory `qa_api/` and from there execute the tests by simply running the command `pytest`.

Five tests should pass, and 2 are expected to fail (`xfail`).
