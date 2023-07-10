import PostList from "@/components/PostList";
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
                <h1>{postsResponse?.feed.title}</h1>
                <PostList posts={postsResponse?.posts} />
            </>
        )
    )

}

export default App;