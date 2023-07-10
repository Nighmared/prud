import { useEffect, useState } from "react";
import { Feed, readFeeds } from "@/util/prud";
import FeedContainer from "@/components/FeedContainer";
import FeedList from "@/components/FeedList";

const App = () => {
    const [feeds, setFeeds] = useState<Feed[]>([])
    useEffect(() => {
        readFeeds(setFeeds);
    }, [])


    return (
        <main>
            < h1 > Hello!</h1 >
            <div>
                <FeedList feeds={feeds} />
            </div>
        </main>
    )
}

export default App;