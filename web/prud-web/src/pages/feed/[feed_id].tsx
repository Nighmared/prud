import { Grid, Typography } from "@mui/material";
import { ReadPostsResponse, fetchReadPosts, isAdmin } from "@/util/prud";
import { useEffect, useState } from "react";

import PostList from "@/components/PostList";
import TitleBar from "@/components/TitleBar";
import { useRouter } from "next/router";

const App = () => {
  const router = useRouter();
  const [postsResponse, setPostsResponse] = useState<ReadPostsResponse>();
  const [needToLoadPosts, setNeedToLoadPosts] = useState(true);
  const [userIsAdmin, setIsAdmin] = useState(false);
  useEffect(() => {
    if (!router.isReady) return;
    const feedId = Number.parseInt(router.query.feed_id as string);
    if (needToLoadPosts) {
      fetchReadPosts(feedId, setPostsResponse);
      setNeedToLoadPosts(false);
    }
    setIsAdmin(isAdmin());
  }, [router.isReady, router.query.feed_id, needToLoadPosts]);

  const reloadPosts = () => {
    setNeedToLoadPosts(true);
  };

  return (
    postsResponse && (
      <main>
        <TitleBar
          backButton={true}
          title={postsResponse.feed.title}
          titleLink={postsResponse.feed.url}
        />
        {!postsResponse.feed.enabled && (
          <Typography
            variant="subtitle1"
            bgcolor={"hotpink"}
            color={"white"}
            align="center"
          >
            Feed is currently disabled because it was unreachable, so some posts
            might be missing
          </Typography>
        )}
        <Grid container spacing={1}>
          <Grid item xs={2} />
          <Grid item xs={8}>
            <PostList
              posts={postsResponse?.posts}
              userIsAdmin={userIsAdmin}
              reloadPostsCallback={reloadPosts}
            />
          </Grid>
        </Grid>
      </main>
    )
  );
};

export default App;
