import { useState, useEffect} from 'react'
import './App.css'

function App() {

  const [data, setData] = useState();
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:4321/ws");

    ws.onopen = () => {
      console.log("Connected!");
    }

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      setData(msg);
    }

    ws.onclose = () => {
      console.log("DC'd");
    }

    return () => ws.close();
  }, []);
  return (
    <>
      <div>
        {!data && <div>No Data Yet</div>}
      </div>
      <div>{data}</div>
    </>
  )
}

export default App
