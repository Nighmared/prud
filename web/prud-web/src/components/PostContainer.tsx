import { Post } from "@/util/prud";
import { Divider, ListItem, ListItemText, Typography } from "@mui/material";

interface Props {
    post: Post;
}

const PostContainer: React.FC<Props> = ({ post }) => {
    const published_txt = new Intl.DateTimeFormat("en-US", { year: "numeric", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" }).format(post.published * 1000)
    const linkWithHttpEnsured = post.link.startsWith("http") ? post.link : `https://${post.link}`
    return (
        <>
            <ListItem alignItems="center">
                <ListItemText>
                    <a className="hover:underline" href={linkWithHttpEnsured} target="_blank">
                        <Typography variant="h4">{post.title}</Typography>
                        <Typography variant="subtitle1">{published_txt}</Typography>
                        <Typography variant="body1">{post.summary.substring(0, 100)}</Typography>
                    </a>

                </ListItemText>
            </ListItem>
            <Divider />
        </>
    )
}


export default PostContainer