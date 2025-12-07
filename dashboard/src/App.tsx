import { useState, useEffect} from 'react'
import './App.css'

function App() {

  const [data, setData] = useState();
  const [isConnected, setIsConnected] = useState(false);
  
  useEffect(() => {
    console.log(import.meta.env.VITE_CONSUMER_WS_URL)
    const ws = new WebSocket(import.meta.env.VITE_CONSUMER_WS_URL);

    ws.onopen = () => {
      console.log("Connected!");
      setIsConnected(true);
    }

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      setData(msg);
    }

    ws.onclose = () => {
      console.log("DC'd");
      setIsConnected(false);
    }

    return () => ws.close();
  }, []);
  return (
    <>
      <div className="absolute top-5 left-5 z-1">
        Status: {isConnected ? <span className="bg-green-500">Connected</span> : <span className="bg-red-500">Disconnected</span>}
      </div>
      <div>
        {!data && <div>No Data Yet</div>}
      </div>
      <div>{data}</div>
    </>
  )
}

export default App
