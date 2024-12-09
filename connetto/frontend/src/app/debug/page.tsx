"use client";

import { authenticatedRequest } from "@/utils/api";

export default function Page() {
    const handleTestRequest = async () => {
        try {
            const response = await authenticatedRequest("http://localhost:8000/api/user-profile/", "POST", {
                username: "testuser",
                fullName: "Test User",
                furigana: "テストユーザー",
                gender: "male",
                birthYear: 1990,
                joinYear: 2020,
                department: "Engineering",
                station: "Tokyo",
            });

            console.log("API Response:", response.data);
            alert("リクエスト成功！ユーザーが登録されました。");
        } catch (error) {
            console.error("API Error:", error);
            alert("リクエストに失敗しました。エラー内容をコンソールで確認してください。");
        }
    };

    return (
        <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
            <h1>APIデバッグページ</h1>
            <p>このページでは、バックエンドAPIへのリクエストをテストできます。</p>
            <button
                onClick={handleTestRequest}
                style={{
                    padding: "10px 20px",
                    backgroundColor: "#0070f3",
                    color: "#fff",
                    border: "none",
                    borderRadius: "5px",
                    cursor: "pointer",
                }}
            >
                APIリクエストを実行
            </button>
        </div>
    );
}
