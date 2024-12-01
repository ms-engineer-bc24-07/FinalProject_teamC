import React from "react";
import { useParams } from "next/navigation";

const mockNotifications = [
    {
        id: 1,
        title: "【登録完了】",
        body: "行きたい登録が完了しました！ありがとうございます。",
        timestamp: "2024-12-01 18:23",
    },
    {
        id: 2,
        title: "【リマインド：本日開催】",
        body: "本日、12月19日（火）18時開催です。ご参加お忘れなく！",
        timestamp: "2024-12-01 11:45",
    },
    ];

    export default function NotificationDetailPage() {
    const params = useParams(); // パラメータ（:id）を取得
    const notificationId = Number(params.id);
    const notification = mockNotifications.find((n) => n.id === notificationId);

    if (!notification) {
        return <p>通知が見つかりません。</p>;
    }

    return (
        <div>
        <h1>{notification.title}</h1>
        <p>{notification.body}</p>
        <p>{notification.timestamp}</p>
        </div>
    );
}
