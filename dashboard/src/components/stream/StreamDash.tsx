import { useState, useEffect} from 'react'
import './App.css'
import StreamCell from './StreamCell';
import StreamRow from './StreamRow';
import Header from '../header/Header';


function StreamDash() {

  type SpreadBook  = {
    [security: string] :
    {
      topBid: string;
      topAsk: string;
      spread: string;
    };
  }

  type SpreadBookRow = {
    security: string;
    topBid: string;
    topAsk: string;
    spread: string;
  }
  const [data, setData] = useState<SpreadBook>({});
  const [isConnected, setIsConnected] = useState(false);

  const [isTableReady, setTableReady] = useState<boolean>();
  
  const websocketUrl = import.meta.env.VITE_CONSUMER_WS_URL;
  useEffect(() => {
    // Get entire table first
    const fetchTable  = async () => {
      try {
        const response = await fetch(import.meta.env.VITE_CONSUMER_HTTP_URL + "/get-all-spread");
        const firstView: SpreadBook = await response.json();
        setData(firstView);
        setTableReady(true);
      } catch(error) {
        console.error("Error fetching data: " + error);
      }
    }
    !isTableReady && fetchTable();
    // Websocket
    console.log(import.meta.env.VITE_CONSUMER_WS_URL)
    const ws = new WebSocket(websocketUrl);

    ws.onopen = () => {
      console.log("Connected!");
      setIsConnected(true);
    }

    ws.onmessage = (event) => {
      // Can't update without first snapshot
      if(!isTableReady) {
        return;
      }
      // Merge in new row
      const msg: SpreadBookRow = JSON.parse(event.data);
      const {security, ...values} = msg;
      setData(prev => ({
          ...prev,
          [security] : {
            ...prev[security],
            ...values,
          }
        }))
    }

    ws.onclose = () => {
      console.log("DC'd");
      setIsConnected(false);
    }

    return () => ws.close();
  }, [isTableReady]);
  
  return (
    <div className="w-[100vw] grid grid-cols-16">
      <Header
        isConnected={isConnected}
        websocketUrl={websocketUrl}
      />
      <div className="grid grid-cols-8 col-start-2 col-span-14">
        <StreamRow key={"titleRow"}>
              <StreamCell data={"Security"} isTitle={true}/>
              <StreamCell data={"Top Bid"} isTitle={true}/>
              <StreamCell data={"Top Ask"} isTitle={true}/>
              <StreamCell data={"Spread"} isTitle={true}/>
        </StreamRow>
        {(!data || Object.entries(data).length == 0) && <div className="grid col-span-8">No Data Yet</div>}

        {data && Object.entries(data).length != 0 && Object.entries(data).map(([security, {topBid, topAsk, spread}]) => {
          return(
            <StreamRow key={security}>
              <StreamCell data={security}/>
              <StreamCell data={topBid}/>
              <StreamCell data={topAsk}/>
              <StreamCell data={spread}/>
            </StreamRow>
          )
        })}
      </div>
    </div>
  )
}

export default StreamDash
