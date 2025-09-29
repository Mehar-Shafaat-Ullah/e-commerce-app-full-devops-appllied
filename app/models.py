import psycopg2
from psycopg2.extras import RealDictCursor

class Product:
    def __init__(self, id, name, price):
        self.id=id; self.name=name; self.price=price

    def to_dict(self):
        return {"id": self.id, "name": self.name, "price": float(self.price)}

    @staticmethod
    def _conn(db_url):
        return psycopg2.connect(db_url, cursor_factory=RealDictCursor)

    @staticmethod
    def create(db_url, name, price):
        with Product._conn(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id, name, price", (name, price))
                row = cur.fetchone()
                return Product(row['id'], row['name'], row['price'])

    @staticmethod
    def list_all(db_url):
        with Product._conn(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, price FROM products ORDER BY id")
                rows = cur.fetchall()
                return [Product(r['id'], r['name'], r['price']) for r in rows]

    @staticmethod
    def get_by_id(db_url, id):
        with Product._conn(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, name, price FROM products WHERE id=%s", (id,))
                r = cur.fetchone()
                if not r: return None
                return Product(r['id'], r['name'], r['price'])

    @staticmethod
    def update(db_url, id, name=None, price=None):
        with Product._conn(db_url) as conn:
            with conn.cursor() as cur:
                # fetch existing
                cur.execute("SELECT id, name, price FROM products WHERE id=%s", (id,))
                r = cur.fetchone()
                if not r: return None
                new_name = name if name is not None else r['name']
                new_price = price if price is not None else r['price']
                cur.execute("UPDATE products SET name=%s, price=%s WHERE id=%s RETURNING id, name, price", (new_name, new_price, id))
                row = cur.fetchone()
                return Product(row['id'], row['name'], row['price'])

    @staticmethod
    def delete(db_url, id):
        with Product._conn(db_url) as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM products WHERE id=%s RETURNING id", (id,))
                r = cur.fetchone()
                return bool(r)

def init_db(db_url):
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                price NUMERIC NOT NULL
            )
            """)
            conn.commit()
