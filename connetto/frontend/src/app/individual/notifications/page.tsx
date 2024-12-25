"use client";

import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import NotificationCard from "@/components/notifications/NotificationCard/NotificationCard";
import DrawerAppBar from "@/components/layout/DrawerAppBar/DrawerAppBar";
import BottomMenu from "@/components/layout/BottomMenu/BottomMenu";
import api from "@/utils/api";

type Notification = {
    id: number;
    title: string;
    body: string;
    created_at: string;
    is_read: boolean;
};

export default function NotificationsPage() {
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const router = useRouter();

    const fetchNotifications = async () => {
        try {
            const response = await api.get("/notifications/");
            setNotifications(response.data);
        } catch (error) {
            console.error("通知の取得に失敗しました:", error);
        }
    };

    useEffect(() => {
        fetchNotifications();
    }, []);

    const handleCardClick = (id: number) => {
        router.push(`/individual/notifications/${id}`); 
    };

    return (
        <div>
            <DrawerAppBar />
            <div style={{ marginTop: "40px" }}>
                {notifications.map((notification) => (
                    <NotificationCard
                        key={notification.id} 
                        id={notification.id} 
                        title={notification.title}
                        body={notification.body}
                        timestamp={notification.created_at}
                        isRead={notification.is_read}
                        onClick={() => handleCardClick(notification.id)}
                    />
                ))}
            </div>
            <BottomMenu />
        </div>
    );
}
