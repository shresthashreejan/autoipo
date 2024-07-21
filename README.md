# AutoIPO

This script automates logging into Meroshare and applying for IPOs or FPOs for lazy people (like me).

1. **Clone Repository**

    ```bash
    git clone https://github.com/shresthashreejan/autoipo.git
    cd autoipo
    ```

2. **Setup Virtual Environment (Optional, but recommended)**

    ```bash
    python3 -m venv venv
    # Windows
    venv\Scripts\activate
    # Unix / MacOS
    source venv/bin/activate
    ```

3. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4. **Setup User Data**

    ```json
    {
        "users": [
            {
                "dp": "user01_depository_participants_value",
                "username": "user01_username",
                "password": "user01_password",
                "crn": "user01_crn",
                "pin": "user01_transaction_pin"
            },
            {
                "dp": "user02_depository_participants_value",
                "username": "user02_username",
                "password": "user02_password",
                "crn": "user02_crn",
                "pin": "user02_transaction_pin"
            },
            {
                "dp": "user03_depository_participants_value",
                "username": "user03_username",
                "password": "user03_password",
                "crn": "user03_crn",
                "pin": "user03_transaction_pin"
            }
        ]
    }
    ```

5. **Run Script**
    ```bash
    python3 main.py
    ```
