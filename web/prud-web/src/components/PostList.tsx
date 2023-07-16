import { Post } from "@/util/prud"
import { List } from "@mui/material"
import PostContainer from "./PostContainer"

interface Props {
    posts: Post[]
}

const PostList: React.FC<Props> = ({ posts }) => {

    return (
        <>


            <List>
                {posts.map((p, i) => <li key={i}><PostContainer post={p} /></li>)}
            </List>
        </>
    )
}


export default PostList