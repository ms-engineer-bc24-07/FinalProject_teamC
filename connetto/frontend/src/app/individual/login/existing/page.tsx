"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { signInWithEmailAndPassword } from "firebase/auth";
import { auth } from "@/utils/firebase";
import BackButton from "@/components/common/BackButton/BackButton";
import InputField from "@/components/common/InputField/InputField";
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";

export default function Existing() {
    const router = useRouter();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState<string | null>(null);

    const handleLogin = async (e: React.MouseEvent<HTMLButtonElement>) => {
        e.preventDefault(); // フォームのデフォルト動作を防ぐ

        try {
            // Firebase Authenticationを利用してログイン
            await signInWithEmailAndPassword(auth, email, password);
            console.log("ログイン成功");

            // ログイン成功後の画面遷移
            router.push("/individual/participation"); 
        } catch (err) {
            console.error("ログイン失敗:", err);
            setError("メールアドレスまたはパスワードが正しくありません。");
        }
    };

return (
    <div>
        <BackButton/>
        <form
            onSubmit={(e) => {
                e.preventDefault(); 
                handleLogin(e as unknown as React.MouseEvent<HTMLButtonElement>);
            }}
        >
            <InputField 
                type="email" 
                placeholder="メールアドレス"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
            <InputField 
                type="password" 
                placeholder="パスワード" 
                value={password}
                onChange={(e) => setPassword(e.target.value)}
            />
            {error && <p style={{ color: "red", marginTop: "10px" }}>{error}</p>}
            <PrimaryButton onClick={(e) => handleLogin(e)}>ログイン</PrimaryButton>
        </form>
    </div>
    );
}
