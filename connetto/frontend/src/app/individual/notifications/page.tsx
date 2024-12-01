"use client";

import React from "react";
import { useRouter } from "next/navigation";
import NotificationCard from "@/components/NotificationCard/NotificationCard";
import DrawerAppBar from "@/components/Header/DrawerAppBar";
import BottomMenu from "@/components/BottomMenu/BottomMenu";


const mockNotifications = [
    {
        id: 1,
        title: "【登録完了】",
        body: "行きたい登録が完了しました！ありがとうございます。",
        timestamp: "2024-12-01 18:23",
        isRead: false,
    },
    {
        id: 2,
        title: "【リマインド：本日開催】",
        body: "本日、12月19日（火）18時開催です。ご参加お忘れなく！",
        timestamp: "2024-12-01 11:45",
        isRead: true,
    },
];

export default function NotificationsPage() {
    const router = useRouter();

    const handleCardClick = (id: number) => {
        router.push(`/notifications/${id}`); // 動的ルートに遷移
    };

    return (
        <div>
            <DrawerAppBar />
            <div style={{ marginTop: '40px' }}>
                {mockNotifications.map((notification) => (
                <NotificationCard
                    key={notification.id}
                    title={notification.title}
                    body={notification.body}
                    timestamp={notification.timestamp}
                    isRead={notification.isRead}
                    onClick={() => handleCardClick(notification.id)}
                />
                ))}
            </div>
            <BottomMenu />
        </div>
    );
}
