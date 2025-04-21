
# Django PayPal Integration Project

This is a Django web application that integrates PayPal for processing payments in Sandbox mode. It allows users to browse projects, purchase them via PayPal, and view transaction details. The project uses PayPal webhooks for real-time payment notifications and logs transaction data for debugging.

## Features

- **Project Listing**: Displays projects with name, price (using django-money), and image.
- **Checkout**: PayPal payment form for purchasing projects in Sandbox mode.
- **Payment Status**: Success and failure pages with project details.
- **Transaction History**: View transaction details in the Django admin or a dedicated page.
- **Webhooks**: Processes `PAYMENT.SALE.COMPLETED` events to update project status and store transaction data.
- **Logging**: Debug logs for checkout and webhook events to troubleshoot issues like `INVALID_BUSINESS_ERROR`.

## Prerequisites

- Python 3.8+
- PayPal Sandbox account (https://developer.paypal.com/)
- Ngrok for local webhook testing (https://ngrok.com/)
- SQLite (default) or another database
- Git

## Installation

### Clone the Repository:

```bash
git clone (https://github.com/fotsoeddy/django-paypal-integration.git)
cd django-paypal-integration
```

### Set Up Virtual Environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Install Dependencies:

```bash
pip install -r requirements.txt
```

### Configure Environment Variables:

Create a `.env` file in the project root:

```bash
touch .env
```

Add the following, replacing placeholders with your PayPal Sandbox credentials:

```
PAYPAL_RECEIVER_EMAIL=sb-your-business-email@business.example.com
PAYPAL_CLIENT_ID=your-sandbox-client-id
PAYPAL_CLIENT_SECRET=your-sandbox-client-secret
PAYPAL_WEBHOOK_ID=your-webhook-id
```

Get credentials from the [PayPal Developer Dashboard](https://developer.paypal.com/).

### Apply Migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser:

```bash
python manage.py createsuperuser
```

### Set Up Ngrok for Webhooks:

```bash
sudo snap install ngrok
ngrok config add-authtoken your-ngrok-auth-token
ngrok http 8000
```

Configure PayPal Webhook to point to `https://your-ngrok-url.ngrok-free.app/webhook/`.

## Project Structure

- `myproject/`: Django project settings and URLs.
- `payments/`: App containing models, views, URLs, and templates.
  - `models.py`: Project and Transaction models.
  - `views.py`: Views for listing, checkout, status, webhook, transactions.
  - `urls.py`: URL patterns.
  - `templates/payments/`: HTML templates.
- `media/projects/`: Project images.
- `debug.log`: Debug logs.

## Usage

### Run the Server:

```bash
python manage.py runserver
```

Ensure Ngrok is running for webhooks.

### Add Projects:

- Admin URL: `http://localhost:8000/admin/`

### Test a Purchase:

- Visit: `http://localhost:8000/`
- Checkout via Sandbox Personal account.

### View Transaction Details:

- Admin: `http://localhost:8000/admin/payments/transaction/`
- Page: `http://localhost:8000/transactions/`
- Logs: Check `debug.log`

## Test Webhooks

Use [Webhook Simulator](https://developer.paypal.com/) to send events.

## Troubleshooting

- `INVALID_BUSINESS_ERROR`: Ensure `.env` matches verified Sandbox business email.
- No webhook events: Check Ngrok and webhook URL.
- No transactions: Ensure model is migrated and webhook is received.

## Development Notes

- Sandbox mode enabled.
- Debug logging in `debug.log`.
- Models: Project and Transaction.
- Handles webhook events.

## Future Improvements

- User association for transactions.
- Pagination, filtering.
- More webhook event support.
- Performance improvements.
- Authenticated user transaction history.

## Contributing

Feel free to fork the repository, submit issues, or create pull requests to enhance the project.

## License

This project is licensed under the MIT License.
