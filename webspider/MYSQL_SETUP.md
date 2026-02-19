## MySQL setup for WebMaster

1. Create the MySQL database and app user:

   ```sql
   SOURCE sql/mysql_setup.sql;
   ```

2. Set environment variables (example values are in `.env.example`):

   - `DJANGO_DB_ENGINE=mysql`
   - `MYSQL_DATABASE=webmaster_db`
   - `MYSQL_USER=webmaster_user`
   - `MYSQL_PASSWORD=ChangeMe_StrongPassword123!`
   - `MYSQL_HOST=127.0.0.1`
   - `MYSQL_PORT=3306`

3. Install the MySQL driver for Django:

   ```bash
   pip install mysqlclient
   ```

4. Run migrations:

   ```bash
   python manage.py migrate
   ```
