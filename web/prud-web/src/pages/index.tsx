import { useEffect, useState } from "react";
import { Feed, readFeeds } from "@/util/prud";
import FeedContainer from "@/components/FeedContainer";
import FeedList from "@/components/FeedList";
import { AppBar, Container, Typography } from "@mui/material";
import TitleBar from "@/components/titlebar";

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