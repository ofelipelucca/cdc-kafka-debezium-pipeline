curl -Method POST http://localhost:8083/connectors `
  -Headers @{"Content-Type"="application/json"} `
  -InFile ../connectors/postgres-connector.json