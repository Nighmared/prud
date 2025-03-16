import { Feed, LoginState, readFeeds } from "@/util/prud";
import { useEffect, useState } from "react";

import { Container } from "@mui/material";
import FeedList from "@/components/FeedList";
import TitleBar from "@/components/TitleBar";

const App = () => {
  const [feeds, setFeeds] = useState<Feed[]>([]);
  useEffect(() => {
    readFeeds(setFeeds);
  }, []);

  return (
    <main>
      <TitleBar title="Polyring Updater" />
      <Container>
        <FeedList feeds={feeds} />
      </Container>
    </main>
  );
};

export default App;
