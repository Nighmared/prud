import { BackHandOutlined, HomeMaxOutlined, HouseOutlined, KeyboardBackspaceOutlined, KeyboardBackspaceRounded } from "@mui/icons-material";
import { AppBar, ListItem, ListItemIcon, ListItemText, Typography } from "@mui/material"
import Link from "next/link";


interface Props {
    title: string;
    backButton?: boolean;
}

const TitleBar: React.FC<Props> = ({ title, backButton = false }) => {
    return (
        <AppBar position="static">
            <ListItem>
                <ListItemIcon>
                    {backButton && <Link href=".."><KeyboardBackspaceOutlined fontSize="large" /></Link>}
                </ListItemIcon>
                <ListItemText />
                <Typography variant="h2" component="div" align="center">{title}</Typography>
                <ListItemText />
            </ListItem>
        </AppBar>
    )
}

export default TitleBar;