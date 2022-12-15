psql -c "CREATE USER root WITH PASSWORD 'roottoor';"
psql -c "ALTER USER root WITH SUPERUSER;"
psql -c "CREATE DATABASE binbanks WITH OWNER root;"
