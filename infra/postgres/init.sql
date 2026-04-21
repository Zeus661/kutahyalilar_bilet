-- Create all databases for each service
CREATE DATABASE auth_db;
CREATE DATABASE user_db;
CREATE DATABASE trip_db;
CREATE DATABASE booking_db;
CREATE DATABASE payment_db;

-- Grant all privileges to the main user
GRANT ALL PRIVILEGES ON DATABASE auth_db TO kutahyalilar;
GRANT ALL PRIVILEGES ON DATABASE user_db TO kutahyalilar;
GRANT ALL PRIVILEGES ON DATABASE trip_db TO kutahyalilar;
GRANT ALL PRIVILEGES ON DATABASE booking_db TO kutahyalilar;
GRANT ALL PRIVILEGES ON DATABASE payment_db TO kutahyalilar;
