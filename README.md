# Odoo 17 Development Setup

This project uses Odoo 17 with a PostgreSQL database and Docker for development.

---

## 🐘 Connecting to the Odoo PostgreSQL Database (via DBeaver)

To connect to the `odoo17` PostgreSQL database using **DBeaver**, follow these steps:

### ✅ Docker Setup Assumption

Your PostgreSQL service is exposed like this in `docker-compose.yml`:

```yaml
services:
  db:
    image: postgres:15
    ports:
      - "5543:5432" # Host port 5543 → Container port 5432
    environment:
      POSTGRES_DB: odoo17
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
```

---

### 🔌 DBeaver Configuration

| Field        | Value           |
| ------------ | --------------- |
| **Host**     | `localhost`     |
| **Port**     | `5543`          |
| **Database** | `odoo17`        |
| **Username** | `odoo`          |
| **Password** | `odoo`          |
| **Auth**     | Database Native |

1. Open DBeaver and click `New Database Connection`
2. Select **PostgreSQL**
3. Enter the above values
4. Click **Test Connection**
5. If successful, click **Finish** to connect

---

### 🧠 Tip (psql via Docker)

You can also connect from your Odoo container using:

```bash
docker exec -it <odoo-container> psql -h db -U odoo -d odoo17
```

This is useful for CLI-based inspection and quick debugging.

---

## 📦 Module Information

This project includes a custom-built Odoo module that manages the lifecycle of custom desk manufacturing and integrates with key business processes like sales, inventory, and accounting.
