import { Feed } from "@/util/prud"
import { CancelOutlined, CheckCircleOutline, LanguageOutlined, RssFeedOutlined } from "@mui/icons-material";
import { Divider, ListItem, ListItemButton, ListItemIcon, ListItemText } from "@mui/material";

import Link from "next/link";


interface props {
    feed: Feed;
}

const FeedContainer: React.FC<props> = (({ feed }) => {


    return (
        <>
            <ListItem>
                <ListItemIcon>
                    {feed.enabled ? <CheckCircleOutline /> : <CancelOutlined />}
                </ListItemIcon>
                <Link href={`/feed/${feed.id}`}>
                    <ListItemButton>
                        <ListItemText>{feed.title}</ListItemText>
                    </ListItemButton >
                </Link>
                <ListItemText />
                <ListItemIcon>
                    <a target="_blank" href={feed.feed}><RssFeedOutlined /></a>
                </ListItemIcon>
                <ListItemIcon>
                    <a target="_blank" href={feed.url}><LanguageOutlined /></a>
                </ListItemIcon>
            </ListItem>
            <Divider />
        </>
    )
})

export default FeedContainer