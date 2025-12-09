import {useState} from 'react';

const SimulateBar = () => {

    const [count, setCount] = useState<string>("25");
    const [delay, setDelay] = useState<string>("0.05");
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const handleRunSimulation = async () => 
    {
        try{
            setIsLoading(true);
            const data = await fetch(`${import.meta.env.VITE_PRODUCER_HTTP_URL}/createdata?data_count=${count}&delay=${delay}`, {method: "POST"})
            console.log(data);
        }
        catch(e)
        {
            console.error(e);
        }
        finally{
            setIsLoading(false);
        }
    }
    return(
        <div className="grid grid-cols-3 max-w-[40vw] md:max-w-[30vw] lg:max-w-[20vw]">
            <input
                type="text"
                value={count}
                onChange={(event: React.ChangeEvent<HTMLInputElement>) => setCount(event.target.value)} 
            />
            <input
                type="text"
                value={delay}
                onChange={(event: React.ChangeEvent<HTMLInputElement>) => setDelay(event.target.value)} 
            />
            {!isLoading ? <div onClick={handleRunSimulation} className="cursor-point">Simulate</div> : <div className="bg-green-600">Running...</div>}
        </div>
    )
}

export default SimulateBar;