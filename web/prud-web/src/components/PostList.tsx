import { Post } from "@/util/prud"
import PostContainer from "./PostContainer"

interface Props {
    posts: Post[]
}

const PostList: React.FC<Props> = ({ posts }) => {

    return (
        <>
            <ul>
                {posts.map((p) => <li><PostContainer post={p} /></li>)}
            </ul>
        </>
    )
}


export default PostList