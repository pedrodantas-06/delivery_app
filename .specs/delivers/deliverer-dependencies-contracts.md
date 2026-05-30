# Deliverer — Dependencies & Contracts (Read-only)

Este arquivo especifica apenas contratos de consumo (APIs read-only) que o módulo Deliverer usa.

1) Orders Service (Contract Read-only)
- GET /orders/{order_id}
  - Response 200:
    ```json
    {
      "id": "<uuid>",
      "restaurant_id": "<uuid>",
      "customer_id": "<uuid>",
      "items": [ {"sku":"...","qty":1} ],
      "status": "PAID|PREPARING|READY|CANCELLED",
      "total": 123.45,
      "region": "Zona Sul"
    }
    ```

2) Restaurants Service (Contract Read-only)
- GET /restaurants/{restaurant_id}
  - Response includes address/region minimal:
    ```json
    {"id":"<uuid>","name":"X","region":"Zona Sul","address":"..."}
    ```

3) Customers Service (Contract Read-only)
- GET /customers/{customer_id}
  - Response minimal:
    ```json
    {"id":"<uuid>","name":"João","phone":"119...","address":"...","region":"Zona Sul"}
    ```

4) Payments Service (Contract Read-only)
- GET /payments?order_id={order_id}
  - Response: status and reconciled flag to trust assignment only if payment completed (business decision).

5) Auth / Identity (Contract)
- Introspect / Validate token: `GET /auth/introspect` or JWT public keys (JWKS). Token must expose `sub` and `role`.

6) Notifications (Contract — optional)
- POST /notifications
  - payload example:
    ```json
    {"target":"deliverer:<id>","type":"assignment","body":{"delivery_id":"...","order_id":"..."}}
    ```

Design rules:
- Todas chamadas a serviços externos são read-only. Nenhuma escrita é permitida em serviços externos.
- Timeouts e retries: 500ms timeout, 2 retries com backoff para chamadas externas sensíveis.
- Fallback: se Orders não responder, assignment deve falhar com `external_unavailable` e não criar inconsistências.
