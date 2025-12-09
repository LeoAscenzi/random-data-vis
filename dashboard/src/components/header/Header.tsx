import SimulateBar from "../simulate/SimulateBar";
import StatsBar from "../simulate/StatsBar";

type HeaderProps = {
    isConnected: boolean;
    websocketUrl: string;
}
const Header = ({isConnected, websocketUrl} : HeaderProps) =>
{
    return (
    <div className="grid grid-cols-8 col-span-16 z-1 text-left border-b-1 mb-12">
        <div className="flex flex-row content-start col-span-8 p-1">
            <div className="flex">{websocketUrl} - </div> 
            {isConnected ? <div className="flex bg-green-500 px-1">Connected</div> 
                        : <div className="flex bg-red-500 px-1">Disconnected</div>}
        </div>
        <div className="grid col-span-8 p-1">
            <SimulateBar/>
        </div>
        <div className="grid col-span-8 p-1">
            <StatsBar/>
        </div>
    </div>
    )
}

export default Header;