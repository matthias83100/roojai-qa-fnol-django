#!/bin/bash

# Exit on error
set -e

echo "--- Starting Deployment Process ---"

# 1. Update system and install Nginx
echo "Installing Nginx..."
# We use || true because sometimes unrelated repositories (like Yarn) might have GPG issues
# that shouldn't block installing Nginx.
sudo apt-get update || true
sudo apt-get install -y nginx

# 2. Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# 3. Collect static files
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# 4. Run database migrations
echo "Running database migrations..."
python3 manage.py migrate

# 5. Setup Nginx configuration
echo "Configuring Nginx..."
sudo cp nginx.conf /etc/nginx/nginx.conf

# Check Nginx configuration syntax
echo "Testing Nginx configuration..."
if sudo nginx -t; then
    echo "Nginx configuration is valid. Restarting..."
    sudo service nginx restart
else
    echo "Error: Nginx configuration is invalid. Please check nginx.conf."
    exit 1
fi

# 6. Start Gunicorn
echo "Starting Gunicorn..."
# Kill any existing gunicorn processes to avoid socket conflicts
pkill -f gunicorn || true
python3 -m gunicorn -c gunicorn_config.py fnol_qa.wsgi:application &
sleep 2 # Give gunicorn a moment to start

if pgrep -f gunicorn > /dev/null; then
    echo "Gunicorn started successfully."
else
    echo "Error: Gunicorn failed to start. Check logs."
    exit 1
fi

echo "--- Deployment Complete ---"
echo "Your app should be available on the forwarded port 8080."
echo "Check GitHub Codespaces 'Ports' tab to find the URL."
