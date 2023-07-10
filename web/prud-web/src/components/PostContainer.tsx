import { Post } from "@/util/prud";
import { Divider, ListItem, ListItemText, Typography } from "@mui/material";
import Link from "next/link";

interface Props {
    post: Post;
}

const PostContainer: React.FC<Props> = ({ post }) => {
    const published_txt = new Intl.DateTimeFormat("en-US", { year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }).format(post.published * 1000)
    return (
        <>
            <ListItem>
                <ListItemText />
                <ListItemText>
                    <a href={post.link}>
                        <Typography variant="h4">{post.title}</Typography>
                    </a>
                    <Typography variant="subtitle1">{published_txt}</Typography>
                    {post.summary}

                </ListItemText>
                <ListItemText />
            </ListItem>
            <Divider />
        </>
    )
}


export default PostContainer