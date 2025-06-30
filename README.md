# FoodDelivery Django Project

This is a full-stack Django web application for a food delivery platform, featuring:

* **User Authentication**: Sign up, log in, and log out with secure password hashing and session management.
* **Role-based Views**: Customers browse restaurants and add items to cart; restaurant owners manage their menu.
* **Restaurant & Menu**: List of restaurants, detailed menu pages with AJAX-powered add-to-cart and quantity selection.
* **Shopping Cart**: Dynamic cart persisted in session, with client-side updates and server-side API fallback.
* **Order Management**: Checkout creates an order (Pending), customer can view all orders; restaurant owners can update order status.
* **Reviews**: Customers can leave 1–5 star reviews and comments; reviews displayed with star visualization.
* **Responsive Design**: Bootstrap 5 layout and components ensure mobile-friendly pages.
* **Security & Validation**: CSRF protection, form validation in views and model managers to prevent common vulnerabilities.
* **Backend**: Django,database, custom user model with additional fields (address, phone, user\_type).
* **AJAX/API**: API endpoints for cart count and add-to-cart actions, enabling seamless client-side updates.

---


## Local Setup

 **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/food-delivery.git
   cd food-delivery
   ```
 **Create and activate a virtual environment**

   ```bash
   python -m venv env
   source env/bin/activate    # Linux/macOS
   env\Scripts\activate     # Windows
   ```
 **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```


## Running the Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.



---

## Key URLs & Endpoints

* **Home / Customer Dashboard**: `/`
* **Restaurant Menu**: `/restaurant/<id>/`
* **Add to Cart API**: `/add-to-cart/` 
* **Cart**: `/cart/`
* **Checkout**: `/cart/checkout/`
* **Orders**: `/track/`
* **Submit Review**: `/restaurant/<id>/review/`
* **Cart Count API**: `/api/cart-count/`
* **About Us**: `/about/`

---


⭐ **Thank you for checking out FoodDelivery!** ⭐
