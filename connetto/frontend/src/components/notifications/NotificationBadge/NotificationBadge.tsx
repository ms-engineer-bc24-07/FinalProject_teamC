import React, { useEffect, useState } from "react";
import { Badge } from "@mui/material";
import NotificationsIcon from "@mui/icons-material/Notifications";
import api from "@/utils/api";

type NotificationBadgeProps = {
    className?: string;
};

export default function NotificationBadge({ className }: NotificationBadgeProps) {
    const [unreadCount, setUnreadCount] = useState<number>(0);

    const fetchUnreadCount = async () => {
        try {
            const response = await api.get("/notifications/unread-count/"); // 未読件数を取得
            setUnreadCount(response.data.unread_count);
        } catch (error) {
            console.error("未読件数の取得に失敗しました:", error);
        }
    };

    useEffect(() => {
        fetchUnreadCount(); 
    }, []);

    return (
        <Badge
        badgeContent={unreadCount > 0 ? unreadCount : null} 
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
