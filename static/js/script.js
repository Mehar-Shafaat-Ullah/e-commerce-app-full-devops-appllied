// Load products when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadProducts();
});

// Load all products from API
async function loadProducts() {
    try {
        const response = await fetch('/products');
        const products = await response.json();
        displayProducts(products);
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Display products in the grid
function displayProducts(products) {
    const productsList = document.getElementById('productsList');
    
    if (products.length === 0) {
        productsList.innerHTML = '<div class="loading">No products found. Add some products!</div>';
        return;
    }

    productsList.innerHTML = products.map(product => `
        <div class="product-card" data-product-id="${product.id}">
            <h3>${product.name}</h3>
            <div class="price">$${product.price}</div>
            <div class="product-actions">
                <button class="delete-btn" onclick="deleteProduct(${product.id})">Delete</button>
            </div>
        </div>
    `).join('');
}

// Add new product
document.getElementById('addProductForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const name = document.getElementById('productName').value;
    const price = parseFloat(document.getElementById('productPrice').value);
    
    if (!name || !price) {
        alert('Please fill in all fields');
        return;
    }

    try {
        const response = await fetch('/products', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, price })
        });

        if (response.ok) {
            // Clear form and reload products
            document.getElementById('addProductForm').reset();
            loadProducts();
        } else {
            alert('Error adding product');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error adding product');
    }
});

// Delete product
async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) {
        return;
    }

    try {
        const response = await fetch(`/products/${productId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadProducts(); // Reload the products list
        } else {
            alert('Error deleting product');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error deleting product');
    }
}