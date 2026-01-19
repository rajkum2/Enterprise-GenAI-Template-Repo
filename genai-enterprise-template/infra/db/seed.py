import os
import psycopg

DATABASE_URL = os.environ.get("DATABASE_URL")


def main() -> None:
    if not DATABASE_URL:
        raise SystemExit("DATABASE_URL is required")
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tenants (id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                ("tenant-1", "Default Tenant"),
            )
            cur.execute(
                "INSERT INTO roles (id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                ("role-admin", "admin"),
            )
            cur.execute(
                "INSERT INTO roles (id, name) VALUES (%s, %s) ON CONFLICT DO NOTHING",
                ("role-user", "user"),
            )
            cur.execute(
                "INSERT INTO users (id, tenant_id, email) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                ("user-admin", "tenant-1", "admin@example.com"),
            )
            cur.execute(
                "INSERT INTO users (id, tenant_id, email) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                ("user-1", "tenant-1", "user@example.com"),
            )
            cur.execute(
                "INSERT INTO user_roles (user_id, role_id, tenant_id) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                ("user-admin", "role-admin", "tenant-1"),
            )
            cur.execute(
                "INSERT INTO user_roles (user_id, role_id, tenant_id) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                ("user-1", "role-user", "tenant-1"),
            )
            cur.execute(
                "INSERT INTO documents (id, tenant_id, source_uri, title, acl) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                ("doc-1", "tenant-1", "s3://example-bucket/sample.txt", "Sample Doc", '{"roles": ["user", "admin"]}'),
            )
            cur.execute(
                "INSERT INTO chunks (id, document_id, tenant_id, content, embedding) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
                ("chunk-1", "doc-1", "tenant-1", "Sample content for retrieval.", '[0.1, 0.2, 0.3]'),
            )
        conn.commit()
    print("Seed data inserted")


if __name__ == "__main__":
    main()
