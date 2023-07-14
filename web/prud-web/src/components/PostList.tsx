import { Post } from "@/util/prud"
import PostContainer from "./PostContainer"
import { Container, Grid, List, ListItemText } from "@mui/material"

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