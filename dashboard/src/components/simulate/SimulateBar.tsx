import {useEffect} from 'react';

type SimulateBarProps = {
    count: string;
    delay: string;
    isLoading: boolean;
    setCount: React.Dispatch<React.SetStateAction<string>>;
    setDelay: React.Dispatch<React.SetStateAction<string>>;
    setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
    setProducerRate: React.Dispatch<React.SetStateAction<number>>;
    setConsumerRate: React.Dispatch<React.SetStateAction<number>>;
}
const SimulateBar = ({count, delay, isLoading, setCount, setDelay, setIsLoading, setProducerRate, setConsumerRate} : SimulateBarProps) => {

    const pollStats = async () => 
    {
        try {
            const pollDataResp = await fetch(`${import.meta.env.VITE_CONSUMER_HTTP_URL}/poll-stats`, {method: "GET"})
            const {status, current_count, elapsed} = await pollDataResp.json();
            console.log("Count: ", current_count);
            console.log(parseFloat(elapsed), " seconds");
            setConsumerRate(status == "not_started" ? 0 :
                parseFloat((parseInt(current_count)/parseFloat(elapsed)).toFixed(2))
            );
        }
        catch(e){
            console.error(e);
        }
    }

    useEffect(() =>{
        const id = setInterval(pollStats, 1000);

        return () => 
        {
            clearInterval(id);
        }
    }, []);
    const handleRunSimulation = async () => 
    {
        if(count && delay){
            try{
                setIsLoading(true);
                setProducerRate(0);
                setConsumerRate(0);
                // Prepare stats and set counts to 0
                const isReady = await fetch(`${import.meta.env.VITE_CONSUMER_HTTP_URL}/prepare-stats?data_count=${count}`, {method: "POST"})
                const readyResp = await isReady.json();
                console.log(readyResp)

                // Start test
                const data = await fetch(`${import.meta.env.VITE_PRODUCER_HTTP_URL}/createdata?data_count=${count}&delay=${delay}`, {method: "POST"})
                const testResult = await data.json()
                console.log(testResult.count);
                console.log(testResult.duration);
                setProducerRate(parseFloat((parseInt(testResult.count)/parseFloat(testResult.duration)).toFixed(2)));
            }
            catch(e)
            {
                console.error(e);
            }
            finally{
                setIsLoading(false);
            }
        }
    }



    return(
        <div className="grid col-span-8 md:grid-cols-4 grid-cols-3 max-w-[60vw] md:max-w-[30vw] lg:max-w-[20vw]">
            {!isLoading ? <div onClick={handleRunSimulation} className="cursor-pointer">Simulate</div> : <div className="bg-green-600">Running...</div>}
            <input
                className="max-w-16 text-center bg-[#444]"
                type="text"
                placeholder="count"
                value={count}
                onChange={(event: React.ChangeEvent<HTMLInputElement>) => setCount(event.target.value)} 
            />
            <input
                className="max-w-16 text-center bg-[#444]"
                type="text"
                placeholder="delay"
                value={delay}
                onChange={(event: React.ChangeEvent<HTMLInputElement>) => setDelay(event.target.value)} 
            />
        </div>
    )
}

export default SimulateBar;