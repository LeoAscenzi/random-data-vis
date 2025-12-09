import React, {useEffect, useRef, useState} from 'react';

type StreamCellProps = {
    data: string;
    isTitle?: boolean;

}
const flashDuration = 100; // ms
const StreamCell = React.memo(({data, isTitle} : StreamCellProps) => 
{
    const [isBlinking, setIsBlinking] = useState<boolean>(false);
    const [oldValue, setOldValue] = useState<string>(data);
    const [increased, setIncreased] = useState<boolean>(false);

    useEffect(() => {
        if (!isTitle) { 
            setIsBlinking(true);
            const timeout = setTimeout(() => setIsBlinking(false), 300);
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

    return <div className=
                {
                    `min-h-16 text-center content-center border-1 bg-gray-600 
                    ${isTitle && "border-none bg-gray-900"}
                    ${isBlinking && `bg-${increased ? "green" : "red"}-500 transition-colors duration-${flashDuration} ease-out`}
                    `
                }
        >{data}</div>
});

export default StreamCell;