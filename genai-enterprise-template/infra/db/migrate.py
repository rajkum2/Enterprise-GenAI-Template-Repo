import glob
import os
import psycopg

DATABASE_URL = os.environ.get("DATABASE_URL")


def main() -> None:
    if not DATABASE_URL:
        raise SystemExit("DATABASE_URL is required")
    migrations = sorted(glob.glob("infra/db/migrations/*.sql"))
    if not migrations:
        raise SystemExit("No migrations found")
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "CREATE TABLE IF NOT EXISTS schema_migrations (filename TEXT PRIMARY KEY)"
            )
            applied = {
                row[0]
                for row in cur.execute("SELECT filename FROM schema_migrations").fetchall()
            }
            for path in migrations:
                name = os.path.basename(path)
                if name in applied:
                    continue
                with open(path, "r", encoding="utf-8") as f:
                    cur.execute(f.read())
                cur.execute(
                    "INSERT INTO schema_migrations (filename) VALUES (%s)", (name,)
                )
        conn.commit()
    print("Migrations applied")


if __name__ == "__main__":
    main()
