import { Feed } from "@/util/prud"
import Link from "next/link";


interface props {
    index: Number;
    feed: Feed;
}

const FeedContainer: React.FC<props> = (({ index, feed }) => {


    return (
        <>
            <div>
                <Link href={`/feed/${feed.id}`}>
                    {feed.title}
                </Link>
            </div>
        </>
    )
})

export default FeedContainer