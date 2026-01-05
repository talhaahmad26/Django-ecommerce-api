# 🛒 Django E-commerce API

A fully functional E-commerce Backend API built with Django REST Framework.

## 🚀 Features
- **User Authentication:** JWT based Signup & Login.
- **Product Management:** CRUD operations for products.
- **Shopping Cart:** Add to cart, view cart, update quantity.
- **Order System:** Checkout process with stock management.
- **Stock Validation:** Prevents ordering out-of-stock items.

## 🛠️ Tech Stack
- Django & Django REST Framework
- SQLite (Database)
- JWT (Authentication)

## 📦 How to Run
1. Clone the repo:
   ```bash
   git clone [https://github.com/talhaahmad26/Django-ecommerce-api.git](https://github.com/talhaahmad26/Django-ecommerce-api.git)
2. Install dependencies:
   pip install django djangorestframework djangorestframework-simplejwt
3. Run migrations:
   python manage.py migrate
4.Start server:
python manage.py runserver
