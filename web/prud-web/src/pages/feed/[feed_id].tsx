import PostList from "@/components/PostList";
import TitleBar from "@/components/titlebar";
import { ReadPostsResponse, fetchReadPosts } from "@/util/prud";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";


const App = () => {
    const router = useRouter();
    const [postsResponse, setPostsResponse] = useState<ReadPostsResponse>();
    useEffect(() => {
        if (!router.isReady) return;
        console.log(router.query.feed_id)
        const feedId = Number.parseInt(router.query.feed_id as string);
        fetchReadPosts(feedId, setPostsResponse)
    }, [router.isReady])

    return (
        postsResponse &&
        (
            <>
                <TitleBar backButton={true} title={postsResponse.feed.title} />
                <PostList posts={postsResponse?.posts} />
            </>
        )
    )

}

export default App;