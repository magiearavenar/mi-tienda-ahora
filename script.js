// Funciones para manejar productos
function getProducts() {
    return JSON.parse(localStorage.getItem('products') || '[]');
}

function saveProducts(products) {
    localStorage.setItem('products', JSON.stringify(products));
}

function getCart() {
    return JSON.parse(localStorage.getItem('cart') || '[]');
}

function saveCart(cart) {
    localStorage.setItem('cart', JSON.stringify(cart));
}

// Cargar productos en la página principal
function loadProducts() {
    const products = getProducts();
    const container = document.getElementById('products-container');
    
    if (!container) return;
    
    container.innerHTML = products.map(product => `
        <div class="product-card">
            <img src="${product.image || 'https://via.placeholder.com/200'}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>${product.description || ''}</p>
            <div class="price">$${product.price}</div>
            <button class="btn" onclick="addToCart(${product.id})">Agregar al Carrito</button>
        </div>
    `).join('');
}

// Agregar producto (admin)
function addProduct(e) {
    e.preventDefault();
    
    const name = document.getElementById('product-name').value;
    const price = parseFloat(document.getElementById('product-price').value);
    const image = document.getElementById('product-image').value;
    const description = document.getElementById('product-description').value;
    
    const products = getProducts();
    const newProduct = {
        id: Date.now(),
        name,
        price,
        image,
        description
    };
    
    products.push(newProduct);
    saveProducts(products);
    
    document.getElementById('product-form').reset();
    loadAdminProducts();
    alert('Producto agregado exitosamente');
}

// Cargar productos en admin
function loadAdminProducts() {
    const products = getProducts();
    const container = document.getElementById('admin-products');
    
    if (!container) return;
    
    container.innerHTML = products.map(product => `
        <div class="admin-product">
            <div>
                <strong>${product.name}</strong> - $${product.price}
            </div>
            <button class="btn btn-danger" onclick="deleteProduct(${product.id})">Eliminar</button>
        </div>
    `).join('');
}

// Eliminar producto
function deleteProduct(id) {
    if (confirm('¿Estás seguro de eliminar este producto?')) {
        const products = getProducts().filter(p => p.id !== id);
        saveProducts(products);
        loadAdminProducts();
    }
}

// Agregar al carrito
function addToCart(productId) {
    const products = getProducts();
    const product = products.find(p => p.id === productId);
    
    if (!product) return;
    
    const cart = getCart();
    const existingItem = cart.find(item => item.id === productId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            quantity: 1
        });
    }
    
    saveCart(cart);
    updateCartCount();
    alert('Producto agregado al carrito');
}

// Actualizar contador del carrito
function updateCartCount() {
    const cart = getCart();
    const count = cart.reduce((total, item) => total + item.quantity, 0);
    const countElement = document.getElementById('cart-count');
    if (countElement) {
        countElement.textContent = count;
    }
}

// Cargar carrito
function loadCart() {
    const cart = getCart();
    const container = document.getElementById('cart-items');
    const totalElement = document.getElementById('cart-total');
    
    if (!container) return;
    
    if (cart.length === 0) {
        container.innerHTML = '<p>Tu carrito está vacío</p>';
        totalElement.textContent = '0.00';
        return;
    }
    
    container.innerHTML = cart.map(item => `
        <div class="cart-item">
            <div>
                <strong>${item.name}</strong><br>
                Cantidad: ${item.quantity} x $${item.price}
            </div>
            <div>
                <button class="btn" onclick="changeQuantity(${item.id}, -1)">-</button>
                <button class="btn" onclick="changeQuantity(${item.id}, 1)">+</button>
                <button class="btn btn-danger" onclick="removeFromCart(${item.id})">Eliminar</button>
            </div>
        </div>
    `).join('');
    
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    totalElement.textContent = total.toFixed(2);
}

// Cambiar cantidad
function changeQuantity(id, change) {
    const cart = getCart();
    const item = cart.find(item => item.id === id);
    
    if (item) {
        item.quantity += change;
        if (item.quantity <= 0) {
            removeFromCart(id);
            return;
        }
        saveCart(cart);
        loadCart();
        updateCartCount();
    }
}

// Eliminar del carrito
function removeFromCart(id) {
    const cart = getCart().filter(item => item.id !== id);
    saveCart(cart);
    loadCart();
    updateCartCount();
}

// Vaciar carrito
function clearCart() {
    if (confirm('¿Estás seguro de vaciar el carrito?')) {
        saveCart([]);
        loadCart();
        updateCartCount();
    }
}

// Finalizar compra
function checkout() {
    const cart = getCart();
    if (cart.length === 0) {
        alert('Tu carrito está vacío');
        return;
    }
    
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    alert(`Compra realizada por $${total.toFixed(2)}. ¡Gracias por tu compra!`);
    
    clearCart();
}

// Inicializar con productos de ejemplo si no hay ninguno
function initializeStore() {
    const products = getProducts();
    if (products.length === 0) {
        const sampleProducts = [
            {
                id: 1,
                name: "Producto Ejemplo 1",
                price: 29.99,
                image: "https://via.placeholder.com/200",
                description: "Descripción del producto ejemplo"
            },
            {
                id: 2,
                name: "Producto Ejemplo 2",
                price: 49.99,
                image: "https://via.placeholder.com/200",
                description: "Otro producto de ejemplo"
            }
        ];
        saveProducts(sampleProducts);
    }
}

// Inicializar la tienda cuando se carga la página
initializeStore();