import React from "react";
import { Badge } from "@mui/material";
import NotificationsIcon from "@mui/icons-material/Notifications";

type NotificationBadgeProps = {
    unreadCount: number;
    className?: string;
};

export default function NotificationBadge({ unreadCount, className }: NotificationBadgeProps) {
    return (
        <Badge
        badgeContent={unreadCount > 0 ? unreadCount : null} // 未読件数を表示
        color="error"
        overlap="circular"
        anchorOrigin={{
            vertical: "top",
            horizontal: "right",
        }}
        >
        <NotificationsIcon className={className} />
        </Badge>
    );
}
