"use client";

import React, { useEffect, useState } from "react";
import { useParams, useRouter } from "next/navigation";
import api from "@/utils/api"; 
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";

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
    const router = useRouter();
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
            <h1
                style={{
                    fontSize: "24px",
                    fontWeight: "bold",
                    textAlign: "left",
                    marginBottom: "10px",
                    marginTop: "20px",
                }}
            >
                {notification.title}
            </h1>
            <hr
                style={{
                    border: "none",
                    borderTop: "2px solid #ddd",
                    margin: "15px 0",
                }}
            />
            <p style={{ fontSize: "16px", lineHeight: "1.6", color: "#333", marginBottom: "15px" }}>
                {notification.body}
            </p>
            <p  style={{ fontSize: "14px", color: "#666", textAlign: "right", marginBottom: "20px" }}>
                {new Date(notification.created_at).toLocaleString("ja-JP", {
                    year: "numeric",
                    month: "2-digit",
                    day: "2-digit",
                    hour: "2-digit",
                    minute: "2-digit",
                })}
            </p>
            {renderNotificationDetails()}
            <div style={{ marginTop: "20px" }}>
                <PrimaryButton onClick={() => router.push("/individual/notifications")}>
                    閉じる
                </PrimaryButton>
            </div>
        </div>
    );
}
