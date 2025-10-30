# Flask JWT API (Users + Products) — Docker Ready

API base para un mini CMS con **Usuarios**, **JWT** y **Productos** (compatible con React Admin). Lista para Docker.

## Arranque rápido (dev)
```bash
docker compose up --build
# o make up
```
- API: http://localhost:5000
- Login: POST `/auth/login` → `{ "email":"admin@local","password":"admin" }` (si SEED_ADMIN=1)
- Productos: todas las rutas con JWT (Authorization: Bearer <token>)

## Endpoints
- `POST /auth/login` → `{ "access": "<JWT>" }`
- `GET /products?_start=0&_end=10` (header `X-Total-Count`)
- `GET /products/<id>`
- `POST /products`
- `PUT /products/<id>`
- `DELETE /products/<id>`

## Variables de entorno
Ver `.env.example`.
Para prod usa MySQL/RDS cambiando `SQLALCHEMY_DATABASE_URI`.

## Estructura
```
api/
  app.py
  wsgi.py
  config.py
  extensions.py
  models/
    __init__.py
    user.py
    product.py
  api/
    __init__.py
    auth.py
    products.py
  utils/
    __init__.py
    errors.py
    pagination.py
```
