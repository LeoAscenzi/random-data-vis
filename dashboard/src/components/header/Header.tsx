import {useState} from 'react';
import SimulateBar from "../simulate/SimulateBar";
import StatsBar from "../simulate/StatsBar";

type HeaderProps = {
    isConnected: boolean;
    websocketUrl: string;
}
const Header = ({isConnected, websocketUrl} : HeaderProps) => {
    const [count, setCount] = useState<string>("");
    const [delay, setDelay] = useState<string>("");
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [producerRate, setProducerRate] = useState<number>(0);
    const [consummerRate, setConsumerRate] = useState<number>(0);

    const [testStatus, setTestStatus] = useState<string>("not_started");

    return (
    <div className="grid grid-cols-8 col-span-16 z-1 text-left border-b-1 mb-12">
        <div className="flex flex-row md:justify-start justify-between col-span-8 p-1">
            <div className="flex">{websocketUrl}</div> 
            <div className={`flex bg-${isConnected ? "green" : "red"}-500 px-1 md:mx-2`}>{isConnected ? "Connected" : "Disconnected"}</div> 
        </div>
        <SimulateBar
            count={count}
            setCount={setCount}
            delay={delay}
            setDelay={setDelay}
            isLoading={isLoading}
            setIsLoading={setIsLoading}
            setProducerRate={setProducerRate}
            setConsumerRate={setConsumerRate}
            setTestStatus={setTestStatus}
        />
        <StatsBar
            theoreticalRate= {count && delay && parseFloat(delay) > 0 ? 1/parseFloat(delay) : 0}
            producerRate = {producerRate}
            consumerRate = {consummerRate}
            testStatus={testStatus}
        />
    </div>
    )
}

export default Header;