CREATE TABLE IF NOT EXISTS temperature_data (id SERIAL PRIMARY KEY, location VARCHAR(255), temperature_celsius FLOAT, measurement_date TIMESTAMP)