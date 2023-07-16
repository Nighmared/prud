import FeedList from "@/components/FeedList";
import TitleBar from "@/components/titlebar";
import { Feed, readFeeds } from "@/util/prud";
import { Container } from "@mui/material";
import { useEffect, useState } from "react";

const App = () => {
    const [feeds, setFeeds] = useState<Feed[]>([])
    useEffect(() => {
        readFeeds(setFeeds);
    }, [])


    return (
        <main style={{ margin: "-8px" }}>
            <TitleBar title="Polyring Updater" />
            <Container>
                <FeedList feeds={feeds} />
            </Container>
        </main>
    )
}

export default App;