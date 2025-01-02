"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import api from "@/utils/api"; 

type Notification = {
    id: number;
    title: string;
    body: string;
    created_at: string;
    is_read: boolean;
    type: string;
    data?: Record<string, any>;
};

export default function NotificationDetailPage() {
    const params = useParams(); 
    const notificationId = Number(params.id);
    const [notification, setNotification] = useState<Notification | null>(null);

    const fetchNotificationDetail = async () => {
        try {
            const response = await api.get(`/notifications/${notificationId}/`);
            setNotification(response.data);

            if (!response.data.is_read) {
                await api.patch(`/notifications/${notificationId}/`, { is_read: true });
            }
        } catch (error) {
            console.error("通知の詳細を取得できませんでした:", error);
        }
    };

    useEffect(() => {
        fetchNotificationDetail();
    }, [notificationId]);

    if (!notification) {
        return <p>通知が見つかりません。</p>;
    }

    const renderNotificationDetails = () => {
        if (notification.type === "EVENT_DECISION" && notification.data) {
            return (
                <div>
                    <h3>開催情報</h3>
                    <p>日時: {notification.data.meeting_date}</p>
                    <p>場所: {notification.data.meeting_location}</p>
                    <p>参加人数: {notification.data.participant_count}人</p>
                </div>
            );
        }
        if (notification.type === "MANAGER_DECISION" && notification.data) {
            return (
                <div>
                    <h3>幹事情報</h3>
                    <p>以下のお店から選択してください:</p>
                    <ul>
                        {notification.data.restaurants?.map((restaurant: any, index: number) => (
                            <li key={index}>
                                <a href={restaurant.url} target="_blank" rel="noopener noreferrer">
                                    {restaurant.name}
                                </a>
                                （{restaurant.address}）
                            </li>
                        ))}
                    </ul>
                </div>
            );
        }

        return null;
    };

    return (
        <div>
            <h1>{notification.title}</h1>
            <p>{notification.body}</p>
            <p>{new Date(notification.created_at).toLocaleString("ja-JP", {
                year: "numeric",
                month: "2-digit",
                day: "2-digit",
                hour: "2-digit",
                minute: "2-digit",
            })}</p>
            {renderNotificationDetails()}
        </div>
    );
}
