# Test the Café 53 API with Bruno

1. Open Bruno Desktop.
2. Choose **Open Collection**.
3. Select this `bruno` directory.
4. Select the **Dev** environment in the environment menu.
5. Run **Health**.
6. Run **Create order**. Its post-response script saves the returned `orderId`.
7. Wait two seconds and run **Get order status**.

The final request should return `READY`. The collection contains no credentials;
the API URL is the only environment-specific value.

