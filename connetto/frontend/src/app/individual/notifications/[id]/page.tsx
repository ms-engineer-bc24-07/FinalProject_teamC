"use client";

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import api from "@/utils/api"; // API呼び出し用のユーティリティ

type Notification = {
    id: number;
    title: string;
    body: string;
    created_at: string;
    is_read: boolean;
};

export default function NotificationDetailPage() {
    const params = useParams(); // 動的ルートからIDを取得
    const notificationId = Number(params.id);
    const [notification, setNotification] = useState<Notification | null>(null);

    // 通知詳細を取得
    const fetchNotificationDetail = async () => {
        try {
            const response = await api.get(`/notifications/${notificationId}/`);
            setNotification(response.data);

            // 既読状態に更新
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
        </div>
    );
}
