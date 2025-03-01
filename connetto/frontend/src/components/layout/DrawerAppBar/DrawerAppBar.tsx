import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import CssBaseline from '@mui/material/CssBaseline';
import Divider from '@mui/material/Divider';
import Drawer from '@mui/material/Drawer';
import IconButton from '@mui/material/IconButton';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemText from '@mui/material/ListItemText';
import MenuIcon from '@mui/icons-material/Menu';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import { usePathname, useRouter } from "next/navigation";
import styles from "./DrawerAppBar.module.css";

interface Props {
    window?: () => Window;
}

const drawerWidth = 240;
const navItems = [
    { name: "行きたい登録", path: "/individual/participation" },
    { name: "登録内容確認", path: "/individual/entries" },
    { name: "開催予定", path: "/individual/events?tab=0" },
    { name: "参加履歴", path: "/individual/events?tab=1" },
    { name: "通知", path: "/individual/notifications" },
    { name: "アカウント設定", path: "/individual/settings" },
];

export default function DrawerAppBar(props: Props) {
    const { window } = props;
    const [mobileOpen, setMobileOpen] = React.useState(false);
    const pathname = usePathname();
    const router = useRouter();

    const handleDrawerToggle = () => {
        setMobileOpen((prevState) => !prevState);
    };

    const drawer = (
        <Box onClick={handleDrawerToggle} sx={{ textAlign: 'center' }}>
        <Typography variant="h6" sx={{ my: 2 }}>
            MENU
        </Typography>
        <Divider />
        <List>
            {navItems.map((item) => (
            <ListItem key={item.name} disablePadding>
                <ListItemButton 
                    className={`${styles.listItemButton} ${
                        pathname === item.path ? styles.listItemButtonActive : ""
                    }`}
                        onClick={() =>  router.push(item.path)}
                >
                        <ListItemText primary={item.name} />
                </ListItemButton>
            </ListItem>
            ))}
        </List>
        </Box>
    );

    const container = window !== undefined ? () => window().document.body : undefined;

    return (
        <Box sx={{ display: 'flex'}}>
        <CssBaseline />
        <AppBar 
            component="nav" 
            position="fixed" 
            sx={{ 
                top: 60,
                width: '100%',
                height: '40px',
                zIndex: 1000,
                backgroundColor: '#85cad0',
                boxShadow: 'none',
            }}
        >
            <Toolbar
                sx={{
                    minHeight: '40px',
                    padding: '0 16px',
                }}
            >
            <IconButton
                aria-label="open drawer"
                edge="start"
                onClick={handleDrawerToggle}
                sx={{ 
                    mr: 2, 
                    display: { sm: 'none' },
                    color: '#000',

                }}
            >
                <MenuIcon />
            </IconButton>
            <Typography
                variant="h6"
                component="div"
                sx={{ flexGrow: 1, display: { xs: 'none', sm: 'block' } }}
            >
            </Typography>
            <Box sx={{ display: { xs: 'none', sm: 'block' } }}>
                {navItems.map((item) => (
                <Button key={item.name} sx={{ color: '#fff' }}>
                    {item.name}
                </Button>
                ))}
            </Box>
            </Toolbar>
        </AppBar>
        <nav>
            <Drawer
            container={container}
            variant="temporary"
            open={mobileOpen}
            onClose={handleDrawerToggle}
            ModalProps={{
                keepMounted: true,
            }}
            sx={{
                display: { xs: 'block', sm: 'none' },
                '& .MuiDrawer-paper': { boxSizing: 'border-box', width: drawerWidth },
            }}
            >
            {drawer}
            </Drawer>
        </nav>
        </Box>
    );
}
