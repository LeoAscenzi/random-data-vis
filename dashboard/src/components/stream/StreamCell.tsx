import React, {useEffect, useState} from 'react';

type StreamCellProps = {
    data: string;
    isTitle?: boolean;

}
const StreamCell = React.memo(({data, isTitle} : StreamCellProps) => 
{
    const [isBlinking, setIsBlinking] = useState<boolean>(false);
    const [oldValue, setOldValue] = useState<string>(data);
    const [increased, setIncreased] = useState<boolean>(false);

    useEffect(() => {
        if (!isTitle) { 
            setIsBlinking(true);
            const timeout = setTimeout(() => setIsBlinking(false), 200);
            return () => clearTimeout(timeout);
        }
    }, [data, isTitle]);

    useEffect(() => {
        if(oldValue != data)
        {
            try {
                setIncreased(parseFloat(oldValue) < parseFloat(data));
            }
            catch(e)
            {
                console.error(e)
            }
        }
        setOldValue(data);
    },[data]) 
    return (
        <div className={`
            min-h-16 text-center content-center border-1 bg-gray-600 
            ${isTitle && "border-none bg-gray-900"}
            ${isBlinking && increased && "bg-green-500 transition-colors duration-200 ease-out"}
            ${isBlinking && !increased && "bg-red-500 transition-colors duration-200 ease-out"}
        `}>
            {data}
        </div>
    )
});

export default StreamCell;