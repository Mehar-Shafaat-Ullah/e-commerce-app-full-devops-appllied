# Mock database implementation - no PostgreSQL required

class Product:
    def __init__(self, id, name, price):
        self.id = id
        self.name = name
        self.price = price

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name, 
            "price": float(self.price)
        }

    @staticmethod
    def _conn(db_url):
        # Mock connection - does nothing
        return None

    @staticmethod
    def create(db_url, name, price):
        global _next_id
        new_product = Product(_next_id, name, price)
        _mock_products.append(new_product)
        _next_id += 1
        return new_product

    @staticmethod
    def list_all(db_url):
        return _mock_products.copy()

    @staticmethod
    def get_by_id(db_url, id):
        for product in _mock_products:
            if product.id == id:
                return product
        return None

    
    @staticmethod
    def update(db_url, id, name=None, price=None):
        for product in _mock_products:
            if product.id == id:
                if name is not None:
                    product.name = name
                if price is not None:
                    product.price = float(price)
                return product
        return None

    @staticmethod
    def delete(db_url, id):
        global _mock_products
        for i, product in enumerate(_mock_products):
            if product.id == id:
                _mock_products.pop(i)
                return True
        return False

# In-memory mock database (outside the class)
_mock_products = [
    Product(1, "Laptop", 999.99),
    Product(2, "Wireless Mouse", 29.99),
    Product(3, "Mechanical Keyboard", 79.99),
    Product(4, "Monitor", 199.99)
]

_next_id = 5

def get_db():
    # Mock database connection
    return None

def init_db(db_url):
    # Mock database initialization - does nothing
    print("Running in mock mode - no real database initialized")
    pass
