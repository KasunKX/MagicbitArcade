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
    const handleKeyDown = (event) => {
      console.log(event.key)
      if (event.key === "ArrowUp" || event.key == "w") sendCommand("fwd");
      else if (event.key === "ArrowDown" || event.key == "s") sendCommand("bwd");
      else if(event.key === " ") sendCommand("hit")
    };
  
    const handleKeyUp = (event) => {
      console.log("Key up");
      if (event.key === "ArrowUp" || event.key == "w" || event.key === "ArrowDown" || event.key == "s") sendCommand("stp");
    };
  
    if (connected) {
      window.addEventListener("keydown", handleKeyDown);
      window.addEventListener("keyup", handleKeyUp);
    }
  
    return () => {
      window.removeEventListener("keydown", handleKeyDown);
      window.removeEventListener("keyup", handleKeyUp);
    };
  }, [connected]);
  
  

    
  const sendCommand = (command) => {
    if (client && connected) {
      console.log(`Sending command: ${command}`);
      client.publish(mqttTopic, JSON.stringify({id:"asdfasdfasdfasdf",command:command}), { qos: 0 });
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
