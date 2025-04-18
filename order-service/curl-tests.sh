#!/bin/bash

# Create an order
curl -X POST http://localhost:8082/orders \
     -H "Content-Type: application/json" \
     -d '{"productIds": [idproduit]}'

# Read an order (replace TIMESTAMP with the actual timestamp from the response above)
curl http://localhost:8082/orders/[id] 