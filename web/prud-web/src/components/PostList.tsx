import { Post } from "@/util/prud"
import PostContainer from "./PostContainer"
import { Container, Grid, List } from "@mui/material"

interface Props {
    posts: Post[]
}

const PostList: React.FC<Props> = ({ posts }) => {

    return (
        <Grid container justifyContent="center">
            <List sx={{ width: "70%" }}>
                {posts.map((p) => <li><PostContainer post={p} /></li>)}
            </List>
        </Grid>
    )
}


export default PostList