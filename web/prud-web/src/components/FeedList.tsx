import { Feed } from "@/util/prud"
import FeedContainer from "./FeedContainer"

interface Props {
    feeds: Feed[]
}

const FeedList: React.FC<Props> = ({ feeds }) => {



    return (
        <>
            <div>
                {feeds.map((f: Feed, i: number) => <FeedContainer index={i} feed={f} />)}
            </div>
        </>
    )
}


export default FeedList