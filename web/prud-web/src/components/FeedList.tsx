import { Feed } from "@/util/prud"
import { List } from "@mui/material"
import FeedContainer from "./FeedContainer"

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