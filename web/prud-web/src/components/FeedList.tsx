import { Feed, isAdmin } from "@/util/prud";
import { useEffect, useState } from "react";

import FeedContainer from "./FeedContainer";
import { List } from "@mui/material";
import { useRouter } from "next/router";

interface Props {
  feeds: Feed[];
  refreshFeedsCallback: () => void;
}

const FeedList: React.FC<Props> = ({
  feeds,
  refreshFeedsCallback: feedRefreshCallback,
}) => {
  const [userIsAdmin, setUserIsAdmin] = useState(false);
  const router = useRouter();
  useEffect(() => {
    if (!router.isReady) return;
    setUserIsAdmin(isAdmin());
  }, [router.isReady]);
  return (
    <>
      <List>
        {feeds.map((f: Feed, i: number) => (
          <FeedContainer
            key={i}
            feed={f}
            userIsAdmin={userIsAdmin}
            refreshFeedsCallback={feedRefreshCallback}
          />
        ))}
      </List>
    </>
  );
};

export default FeedList;
