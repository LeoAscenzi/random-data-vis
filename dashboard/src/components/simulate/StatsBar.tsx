type StatsBarProps = {
    theoreticalRate: number;
    producerRate: number;
    consumerRate: number;
}

const StatsBar = ({theoreticalRate, producerRate, consumerRate} : StatsBarProps) => 
{
    return(
        <div className="grid col-span-8 md:grid-cols-4 grid-cols-16 md:max-w-[45vw] lg:max-w-[40vw] pb-1">
            <div className="grid md:col-span-1 col-span-2">Stats</div>
            {/* Theoretical */}
            <div className="grid md:col-span-1 col-span-4 text-center">{theoreticalRate} msg/s</div>
            {/* Producer */}
            <div className="grid md:col-span-1 col-span-5 text-center">{producerRate} msg/s</div>
            {/* Consumer */}
            <div className="grid md:col-span-1 col-span-5 text-center">{consumerRate} msg/s</div>
        </div>
    )
}
export default StatsBar;