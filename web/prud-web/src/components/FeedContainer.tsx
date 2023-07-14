import { Feed } from "@/util/prud"
import { CancelOutlined, CheckCircleOutline, LanguageOutlined, RssFeedOutlined } from "@mui/icons-material";
import { Divider, ListItem, ListItemButton, ListItemIcon, ListItemText, Tooltip } from "@mui/material";

import Link from "next/link";


interface props {
    feed: Feed;
}

const FeedContainer: React.FC<props> = (({ feed }) => {


    return (
        <>
            <ListItem>
                <Tooltip title={feed.enabled ? "Enabled" : "Disabled"}>
                    <ListItemIcon className={feed.enabled ? "text-green-400" : "text-red-500"}>
                        {feed.enabled ? <CheckCircleOutline /> : <CancelOutlined />}
                    </ListItemIcon>
                </Tooltip>
                <Link href={`/feed/${feed.id}`}>
                    <ListItemButton>
                        <ListItemText>{feed.title}</ListItemText>
                    </ListItemButton >
                </Link>
                {/* Find a better way for alignment  */}
                <ListItemText />
                <Tooltip title="Link to RSS Feed">
                    <ListItemIcon>
                        <a target="_blank" href={feed.feed}><RssFeedOutlined className="text-orange-500" /></a>
                    </ListItemIcon>
                </Tooltip>
                <Tooltip title="Link to Blog Homepage">
                    <ListItemIcon>
                        <a target="_blank" href={feed.url}><LanguageOutlined className="text-blue-500" /></a>
                    </ListItemIcon>
                </Tooltip>
            </ListItem>
            <Divider />
        </>
    )
})

export default FeedContainer