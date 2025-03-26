import React, { useState, useEffect } from "react";
import mqtt from "mqtt";

const MqttController = () => {
  const [client, setClient] = useState(null);
  const [connected, setConnected] = useState(false);

  // MQTT connection details for WebSocket
  const mqttServer = "wss://broker.emqx.io:8084/mqtt";
  const mqttTopic = "magicgames/1";


  useEffect(()=> {
    const mqttClient = mqtt.connect(mqttServer, {
      clientId: "clientId-" + new Date().getTime(),
    });
    mqttClient.on("connect", () => {
      console.log("Connected to MQTT broker");
      setConnected(true);
      mqttClient.subscribe(mqttTopic);
      setClient(mqttClient);
    });
  },[])



  useEffect(() => {
    if (connected) {
      window.addEventListener("keydown", (event) => {
          if (event.key === "ArrowUp") {
            sendCommand("fwd");
          } else if (event.key === "ArrowDown") {
            sendCommand("bwd");
          } else if (event.key === " ") {
            sendCommand("stp");
          }
        }
      );
  }
    return () => {
      window.removeEventListener("keydown", () => {});
    }
    
  },[connected]);

    
  const sendCommand = (command) => {
    if (client && connected) {
      console.log(`Sending command: ${command}`);
      client.publish(mqttTopic, JSON.stringify({id:"asdfasdfasdfasdf",command:command}));
    } else {
      console.log("MQTT client is not connected.");
    }
  };

  return (
    <div className="mqtt-controller">
      <h2>MQTT Controller</h2>
      <div>
        <button onClick={() => sendCommand("fwd")}>Up</button>
        <button onClick={() => sendCommand("bwd")}>Down</button>
        <button onClick={() => sendCommand("stp")}>Space</button>
      </div>
      {connected ? (
        <p>Connected to MQTT Broker</p>
      ) : (
        <p>Connecting to MQTT Broker...</p>
      )}
    </div>
  );
};

export default MqttController;
