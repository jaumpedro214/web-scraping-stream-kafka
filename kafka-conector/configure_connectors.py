from time import sleep
import requests

CONNECTORS = [
    {
        "name": "produtos_connector",
        "config": {
            "topics": "produtos",
            
            "connector.class":
                "io.confluent.connect.jdbc.JdbcSinkConnector",
            "tasks.max": "1",
            
            "connection.url": "jdbc:postgresql://postgres:5432/produtos",
            "connection.user": "usuario",
            "connection.password": "123",

            "auto.create": "true",
            "insert.mode": "upsert",
            "pk.fields": "id",
            "pk.mode": "record_value",
            
            "erroros.tolerance": "all",
        }
    }
]
    
# Try write the connectors to the debezium server
for connector in CONNECTORS:
    response = requests.post(
        "http://localhost:8083/connectors",
        headers={
            "Content-Type": "application/json"
        },
        json=connector
    )
    print(response)
    print(response.json())
    print("")
    print("")