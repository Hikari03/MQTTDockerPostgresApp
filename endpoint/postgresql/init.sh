psql postgresql://postgres:varilamysickakasicku@localhost:5432/temperature_data -c "CREATE TABLE IF NOT EXISTS temperature_data (id SERIAL PRIMARY KEY,city VARCHAR(255),temperature_celsius FLOAT,measurement_date TIMESTAMP);"
RUN chmod +x /docker-entrypoint-initdb.d/init.sh
