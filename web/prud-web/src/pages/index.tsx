import { Feed, LoginState, readFeeds } from "@/util/prud";
import { useEffect, useState } from "react";

import { Container } from "@mui/material";
import FeedList from "@/components/FeedList";
import Footer from "@/components/Footer";
import TitleBar from "@/components/TitleBar";

const App = () => {
  const [feeds, setFeeds] = useState<Feed[]>([]);
  const [needRefresh, setNeedRefresh] = useState(true);
  const refreshCallback = () => setNeedRefresh(true);

  useEffect(() => {
    if (needRefresh) {
      readFeeds(setFeeds);
      setNeedRefresh(false);
    }
  }, [needRefresh]);

  return (
    <main>
      <TitleBar title="Polyring Updater" />
      <Container>
        <FeedList feeds={feeds} refreshFeedsCallback={refreshCallback} />
      </Container>
      <Footer />
    </main>
  );
};

export default App;
