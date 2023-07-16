import '@/assets/tailwind.css';
import { KeyboardBackspaceOutlined } from "@mui/icons-material";
import { AppBar, ListItem, ListItemIcon, ListItemText, Typography } from "@mui/material";
import Link from "next/link";

interface Props {
    title: string;
    backButton?: boolean;
    titleLink?: string;
}

const TitleBar: React.FC<Props> = ({ title, backButton = false, titleLink = "/" }) => {
    return (
        <AppBar className="bg-slate-800" position="sticky" sx={{ width: "100%" }}>
            <ListItem>
                <ListItemIcon>
                    {backButton && <Link href=".."><KeyboardBackspaceOutlined fontSize="large" /></Link>}
                </ListItemIcon>
                <ListItemText />
                <a className="hover:underline" href={titleLink} target={titleLink == "/" ? "" : "_blank"}><Typography variant="h2" component="div" align="center">{title}</Typography></a>
                <ListItemText />
            </ListItem>
        </AppBar >
    )
}

export default TitleBar;