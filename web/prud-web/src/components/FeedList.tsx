import { Feed } from "@/util/prud"
import FeedContainer from "./FeedContainer"
import { List } from "@mui/material"

interface Props {
    feeds: Feed[]
}

const FeedList: React.FC<Props> = ({ feeds }) => {



    return (
        <>
            <List>
                {feeds.map((f: Feed, i: number) => <FeedContainer key={i} feed={f} />)}
            </List>
        </>
    )
}


export default FeedList