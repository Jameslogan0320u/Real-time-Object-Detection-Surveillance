import asyncio
from gmqtt import Client as MQTTClient

async def initialize_mqtt(broker="mqtt.eclipseprojects.io"):
    client = MQTTClient("client-id")
    await client.connect(broker)
    return client

async def send_mqtt_alert(client, topic="home/surveillance", message="Object of interest detected!"):
    client.publish(topic, message)

# Example usage
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    mqtt_client = loop.run_until_complete(initialize_mqtt())
    loop.run_until_complete(send_mqtt_alert(mqtt_client))
