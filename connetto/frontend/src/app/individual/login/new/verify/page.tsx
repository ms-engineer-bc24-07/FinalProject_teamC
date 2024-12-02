"use client";

import { useRouter } from "next/navigation";
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";

export default function VerifyCode() {
    const router = useRouter()

    const navigateToAccount = () => {
        router.push("/individual/login/new/account"); 
    };

    return (
            <div>
                <h1>認証コードを入力</h1>
                <p>
                    認証コードを送信しました。メールに記載された認証コードを入力し、確認ボタンを押してください。
                </p>
                <div>
                    
                </div>
                <PrimaryButton onClick={navigateToAccount}>確認</PrimaryButton>
                <p>認証コードを再送</p>
            </div>
    );
}