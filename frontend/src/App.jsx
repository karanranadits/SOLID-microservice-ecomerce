import { useState, useEffect } from 'react'
import './index.css'

const AUTH_URL = 'http://localhost:8001'
const ORDER_URL = 'http://localhost:8002/api/v1'

const PRODUCTS = [
  { id: 'prod_m1', name: 'IPHONE 13', price: 980, category: 'mobile', img: 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?q=80&w=400&auto=format&fit=crop' },
  { id: 'prod_m2', name: 'IPHONE 12', price: 750, category: 'mobile', img: 'https://images.unsplash.com/photo-1556656793-08538906a9f8?q=80&w=400&auto=format&fit=crop' },
  { id: 'prod_m3', name: 'IPHONE 11', price: 600, category: 'mobile', img: 'https://images.unsplash.com/photo-1591337676887-a4b7f05e5ce0?q=80&w=400&auto=format&fit=crop' },
  { id: 'prod_m4', name: 'IPHONE X', price: 500, category: 'mobile', img: 'https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?q=80&w=400&auto=format&fit=crop' },
  { id: 'prod_w1', name: 'PINK WATCH', price: 870, category: 'watch', img: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=400&auto=format&fit=crop' },
  { id: 'prod_w2', name: 'HEAVY WATCH', price: 680, category: 'watch', img: 'https://images.unsplash.com/photo-1546868871-7041f2a55e12?q=80&w=400&auto=format&fit=crop' },
  { id: 'prod_w3', name: 'SPOTTED WATCH', price: 750, category: 'watch', img: 'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?q=80&w=400&auto=format&fit=crop' },
  { id: 'prod_w4', name: 'BLACK WATCH', price: 650, category: 'watch', img: 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?q=80&w=400&auto=format&fit=crop' }
]

function App() {
  const [token, setToken] = useState(localStorage.getItem('token') || '')
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [orders, setOrders] = useState([])
  const [loading, setLoading] = useState(false)
  
  const [showLoginModal, setShowLoginModal] = useState(false)
  const [currentView, setCurrentView] = useState('home') // 'home' | 'orders' | 'cart' | 'checkout'
  
  // Cart State
  const [cart, setCart] = useState([])

  // Billing Details
  const [cardDetails, setCardDetails] = useState({
    card_number: '',
    expiry: '',
    cvv: ''
  })

  useEffect(() => {
    if (token) fetchOrders()
  }, [token])

  const showMessage = (msg, type = 'success') => {
    if (type === 'error') setError(msg)
    else setSuccess(msg)
    setTimeout(() => {
      setError('')
      setSuccess('')
    }, 4000)
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await fetch(`${AUTH_URL}/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Login failed')
      setToken(data.access_token)
      localStorage.setItem('token', data.access_token)
      setShowLoginModal(false)
      showMessage('Logged in successfully!')
    } catch (err) {
      showMessage(err.message, 'error')
    } finally {
      setLoading(false)
    }
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await fetch(`${AUTH_URL}/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Registration failed')
      setToken(data.access_token)
      localStorage.setItem('token', data.access_token)
      setShowLoginModal(false)
      showMessage('Registered and logged in!')
    } catch (err) {
      showMessage(err.message, 'error')
    } finally {
      setLoading(false)
    }
  }

  const fetchOrders = async () => {
    try {
      const res = await fetch(`${ORDER_URL}/orders`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      const data = await res.json()
      if (res.ok) setOrders(data)
    } catch (err) {
      console.error(err)
    }
  }

  const addToCart = (product) => {
    const existing = cart.find(item => item.product_id === product.id)
    if (existing) {
      setCart(cart.map(item => item.product_id === product.id ? { ...item, quantity: item.quantity + 1 } : item))
    } else {
      setCart([...cart, { product_id: product.id, name: product.name, price: product.price, quantity: 1 }])
    }
    showMessage(`${product.name} added to cart!`)
  }

  const getCartTotal = () => cart.reduce((sum, item) => sum + (item.price * item.quantity), 0)

  const processCheckout = async (e) => {
    e.preventDefault()
    if (!token) {
      setShowLoginModal(true)
      return
    }

    if (cart.length === 0) {
      showMessage("Cart is empty!", "error")
      return
    }

    setLoading(true)
    try {
      const res = await fetch(`${ORDER_URL}/orders`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          items: cart.map(item => ({ product_id: item.product_id, quantity: item.quantity, price: item.price })),
          payment_details: cardDetails
        })
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.detail || 'Order failed')
      
      if (data.status === 'payment_failed') {
        showMessage(`Order created but payment failed (Saga compensated). Status: ${data.status}`, 'error')
      } else {
        showMessage(`Order placed successfully! Total: $${data.total_amount}`)
      }
      
      setCart([])
      setCardDetails({ card_number: '', expiry: '', cvv: '' })
      fetchOrders()
      setCurrentView('orders')
    } catch (err) {
      showMessage(err.message, 'error')
    } finally {
      setLoading(false)
    }
  }

  const logout = () => {
    setToken('')
    localStorage.removeItem('token')
    setOrders([])
    setCurrentView('home')
  }

  // Views
  const renderProductGrid = (category, title) => (
    <section className="container" style={{ marginBottom: '80px' }}>
      <div className="section-title">
        <h3>{title}</h3>
        <a href="#">GO TO SHOP &rarr;</a>
      </div>
      <div className="product-grid">
        {PRODUCTS.filter(p => p.category === category).map(product => (
          <div key={product.id} className="product-card">
            <div className="product-img-wrapper">
              <img src={product.img} alt={product.name} />
            </div>
            <h4 className="product-title">{product.name}</h4>
            <div className="product-price">${product.price.toFixed(2)}</div>
            <button 
              className="btn btn-outline" 
              onClick={() => addToCart(product)}
              style={{ width: '100%' }}
            >
              Add to Cart
            </button>
          </div>
        ))}
      </div>
    </section>
  )

  const renderHome = () => (
    <>
      <section className="hero">
        <div className="container">
          <div className="hero-text">
            <h1>Your Products<br/>Are Great.</h1>
            <button className="btn" style={{ marginTop: '16px' }} onClick={() => window.scrollTo(0, 500)}>Shop Product</button>
          </div>
          <div className="hero-image">
            <img src="https://images.unsplash.com/photo-1523275335684-37898b6baf30?q=80&w=600&auto=format&fit=crop" alt="Hero Watch" />
          </div>
        </div>
      </section>
      {renderProductGrid('mobile', 'Mobile Products')}
      {renderProductGrid('watch', 'Smart Watches')}
    </>
  )

  const renderCart = () => (
    <section className="container" style={{ padding: '80px 24px', minHeight: '60vh' }}>
      <div className="section-title">
        <h3>Shopping Cart</h3>
      </div>
      {cart.length === 0 ? (
        <p className="text-muted">Your cart is empty.</p>
      ) : (
        <>
          <div className="order-list">
            {cart.map(item => (
              <div key={item.product_id} className="order-item">
                <div>
                  <h4 style={{ marginBottom: '8px' }}>{item.name}</h4>
                  <p className="text-muted" style={{ margin: 0, fontSize: '14px' }}>Qty: {item.quantity}</p>
                </div>
                <div style={{ fontSize: '20px', fontWeight: 600 }}>
                  ${(item.price * item.quantity).toFixed(2)}
                </div>
              </div>
            ))}
          </div>
          <div className="flex justify-between items-center" style={{ marginTop: '32px' }}>
            <h2>Total: ${getCartTotal().toFixed(2)}</h2>
            <button className="btn" onClick={() => setCurrentView('checkout')}>Proceed to Checkout</button>
          </div>
        </>
      )}
    </section>
  )

  const renderCheckout = () => (
    <section className="container" style={{ padding: '80px 24px', minHeight: '60vh', maxWidth: '600px' }}>
      <div className="section-title">
        <h3>Checkout & Billing</h3>
      </div>
      <div className="order-item" style={{ marginBottom: '32px', display: 'block' }}>
        <h4 style={{ marginBottom: '16px' }}>Order Summary</h4>
        <div className="flex justify-between text-muted" style={{ marginBottom: '8px' }}>
          <span>Items ({cart.length})</span>
          <span>${getCartTotal().toFixed(2)}</span>
        </div>
        <div className="flex justify-between text-muted" style={{ marginBottom: '8px' }}>
          <span>Discount (10%)</span>
          <span>-${(getCartTotal() * 0.1).toFixed(2)}</span>
        </div>
        <hr style={{ borderColor: '#e5e5e5', margin: '16px 0' }} />
        <div className="flex justify-between" style={{ fontSize: '20px', fontWeight: 600 }}>
          <span>Total</span>
          <span>${(getCartTotal() * 0.9).toFixed(2)}</span>
        </div>
      </div>

      <form onSubmit={processCheckout}>
        <h4 style={{ marginBottom: '24px' }}>Payment Details (Mock)</h4>
        <div className="form-group">
          <label>Card Number (16 Digits)</label>
          <input 
            type="text" 
            value={cardDetails.card_number} 
            onChange={e => setCardDetails({...cardDetails, card_number: e.target.value})}
            placeholder="1234123412341234"
            required
          />
        </div>
        <div className="flex gap-4">
          <div className="form-group" style={{ flex: 1 }}>
            <label>Expiry (MM/YY)</label>
            <input 
              type="text" 
              value={cardDetails.expiry} 
              onChange={e => setCardDetails({...cardDetails, expiry: e.target.value})}
              placeholder="12/26"
              required
            />
          </div>
          <div className="form-group" style={{ flex: 1 }}>
            <label>CVV</label>
            <input 
              type="text" 
              value={cardDetails.cvv} 
              onChange={e => setCardDetails({...cardDetails, cvv: e.target.value})}
              placeholder="123"
              required
            />
          </div>
        </div>
        <button type="submit" className="btn" style={{ width: '100%', marginTop: '16px' }} disabled={loading}>
          {loading ? 'Processing...' : 'Pay & Place Order'}
        </button>
      </form>
    </section>
  )

  const renderOrders = () => (
    <section className="container" style={{ padding: '80px 24px', minHeight: '60vh' }}>
      <div className="section-title">
        <h3>Your Orders ({orders.length})</h3>
      </div>
      <div className="order-list">
        {orders.length === 0 && <p className="text-muted">No orders placed yet.</p>}
        {orders.map(order => (
          <div key={order.id} className="order-item">
            <div>
              <h4 style={{ marginBottom: '8px' }}>Order #{order.id.split('-')[0].toUpperCase()}</h4>
              <p className="text-muted" style={{ margin: 0, fontSize: '14px' }}>
                Status: <span style={{ color: order.status === 'paid' ? '#059669' : '#dc2626', fontWeight: 600 }}>{order.status}</span>
              </p>
            </div>
            <div style={{ fontSize: '20px', fontWeight: 600 }}>
              ${order.total_amount.toFixed(2)}
            </div>
          </div>
        ))}
      </div>
    </section>
  )

  return (
    <>
      {/* Navigation */}
      <nav className="navbar">
        <div className="container flex justify-between items-center">
          <div className="nav-logo">MiniStore</div>
          <div className="nav-links flex gap-4">
            <button onClick={() => setCurrentView('home')}>Home</button>
            <button onClick={() => setCurrentView('cart')}>
              Cart ({cart.reduce((sum, item) => sum + item.quantity, 0)})
            </button>
            {!token ? (
              <button onClick={() => setShowLoginModal(true)}>Login</button>
            ) : (
              <>
                <button onClick={() => setCurrentView('orders')}>My Orders</button>
                <button onClick={logout}>Logout</button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Global Messages */}
      {error && <div className="message error" style={{ position: 'fixed', top: 80, width: '100%', zIndex: 50 }}>{error}</div>}
      {success && <div className="message success" style={{ position: 'fixed', top: 80, width: '100%', zIndex: 50 }}>{success}</div>}

      {/* Main Content */}
      <main>
        {currentView === 'home' && renderHome()}
        {currentView === 'cart' && renderCart()}
        {currentView === 'checkout' && renderCheckout()}
        {currentView === 'orders' && renderOrders()}
      </main>

      {/* Footer */}
      <footer style={{ background: '#111', color: 'white', padding: '64px 0', textAlign: 'center' }}>
        <div className="container flex-col items-center gap-8">
          <h2 className="nav-logo">MiniStore</h2>
          <div className="flex gap-4 text-muted" style={{ fontSize: '13px' }}>
            <span>© 2026 MiniStore. All rights reserved.</span>
          </div>
        </div>
      </footer>

      {/* Login Modal */}
      {showLoginModal && (
        <div className="modal-overlay" onClick={() => setShowLoginModal(false)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <h3 style={{ marginBottom: '32px', textAlign: 'center' }}>Welcome Back</h3>
            <form>
              <div className="form-group">
                <label>Username</label>
                <input 
                  type="text" 
                  value={username} 
                  onChange={e => setUsername(e.target.value)}
                  placeholder="Enter username"
                />
              </div>
              <div className="form-group" style={{ marginBottom: '40px' }}>
                <label>Password</label>
                <input 
                  type="password" 
                  value={password} 
                  onChange={e => setPassword(e.target.value)}
                  placeholder="Enter password"
                />
              </div>
              <div className="flex-col gap-4">
                <button type="button" className="btn" onClick={handleLogin} disabled={loading}>
                  Login
                </button>
                <button type="button" className="btn btn-outline" onClick={handleRegister} disabled={loading}>
                  Create Account
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  )
}

export default App
