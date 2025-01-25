

# Django IP-Specific Rate Limiting and Blocking

This project is a Django-based application that implements **IP-specific rate limiting** and **dynamic IP blocking** for specific API routes. It allows administrators to manage rate-limiting rules and block IPs directly through the Django admin panel. The project uses Django’s caching framework to efficiently track requests and enforce rate limits.

---

## Description

### What This Project Does:
1. **Rate Limiting**:
   - Enforces custom rate limits for specific IP addresses on specific API paths.
   - Tracks the number of requests made by an IP and restricts further requests if the limit is exceeded.

2. **IP Blocking**:
   - Allows dynamic blocking of specific IPs with a reason provided by the administrator.

3. **Admin Panel Management**:
   - Admins can manage rate-limiting rules and blocked IPs dynamically through the Django admin interface.

4. **Django Cache**:
   - Leverages Django’s built-in caching framework to track and store request data.

---

## Setup Instructions

### Prerequisites
1. Python (>= 3.8)
2. pip for package management

### Installation Steps

#### 1. Clone the Repository
```bash
git clone https://github.com/your-username/django-ip-rate-limiting.git
cd django-ip-rate-limiting
```

#### 2. Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Configure Environment Variables
Create a `.env` file in the root directory and populate it with the required environment variables:

```plaintext
SECRET_KEY=your_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

#### 5. Apply Migrations
Run the following commands to apply database migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

#### 6. Create a Superuser
Create an admin account to access the Django admin panel:
```bash
python manage.py createsuperuser
```

#### 7. Run the Development Server
Start the Django development server:
```bash
python manage.py runserver
```

The application will now be available at `http://127.0.0.1:8000/`.

---

## How to Run the Project

### 1. Access the Admin Panel
Go to `http://127.0.0.1:8000/api/admin/` and log in using the superuser credentials created during setup.

### 2. Add Rate Limiting Rules
1. Navigate to **Rate Limit Rules** in the admin panel.
2. Add a new rule by specifying:
   - **IP Address**: The IP address to apply the rule.
   - **Path**: The API route (e.g., `/api/example/`).
   - **Max Requests**: Maximum allowed requests within the time window.
   - **Window Seconds**: Duration (in seconds) of the time window.

### 3. Block an IP Address
1. Navigate to **IP Block** in the admin panel.
2. Add an IP address to block, along with an optional reason.

### 4. Test Rate Limiting and IP Blocking
Use tools like `curl` or Postman to test the API endpoints.

#### Example (Using curl):
```bash
curl -X GET http://127.0.0.1:8000/api/example/ -H "X-Forwarded-For: 192.168.1.101"
```

- **If the rate limit is exceeded**, you’ll receive:
  ```json
  {
      "error": "Rate limit exceeded. Try again later.",
      "requests_made": 5,
      "max_requests": 5
  }
  ```

- **If the IP is blocked**, you’ll receive:
  ```json
  {
      "error": "Access blocked for this IP"
  }
  ```

---

## Project Structure

The project consists of the following key components:

1. **IPBlock Model**:
   - Stores blocked IP addresses and optional reasons for blocking.

2. **RateLimitRule Model**:
   - Defines rate-limiting rules for specific IP addresses and paths.

3. **Dynamic Middleware**:
   - Implements rate limiting and IP blocking by dynamically checking requests.

4. **Django Cache**:
   - Tracks request counts and enforces limits using Django’s caching framework.

---

## Example `.env` File
Here’s an example `.env` file for this project:

```plaintext
SECRET_KEY=your_secret_key
DEBUG=True
```

---

## Dependencies

The project uses the following Python packages:

| Package                  | Version | Description                                       |
|--------------------------|---------|---------------------------------------------------|
| `Django`                 | 5.1.5   | The core web framework.                          |
| `django-cors-headers`    | 4.6.0   | Enables Cross-Origin Resource Sharing (CORS).    |
| `python-dotenv`          | 1.0.1   | Loads environment variables from `.env` files.   |
| `asgiref`                | 3.8.1   | ASGI framework used by Django for async support. |
| `sqlparse`               | 0.5.3   | SQL parsing library required by Django.          |
| `tzdata`                 | 2025.1  | Timezone support for Django.                     |

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

## Contribution

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch (`feature/your-feature`).
3. Commit your changes.
4. Submit a pull request.

