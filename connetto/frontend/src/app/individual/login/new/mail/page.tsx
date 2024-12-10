"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import InputField from "@/components/common/InputField/InputField";
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";
import BackButton from "@/components/common/BackButton/BackButton";
import { createUserWithEmailAndPassword } from "firebase/auth";
import { auth } from "@/utils/firebase";

export default function MailRegister() {
  const router = useRouter();


    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [error, setError] = useState({
        email: "",
        password: "",
        confirmPassword: "",
        general: "",
    });

    const validateInputs = () => {
        let isValid = true;
        const newError = { email: "", password: "", confirmPassword: "", general: "" };

        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
            newError.email = "メールアドレスの形式が正しくありません。";
            isValid = false;
        }

        if (!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,16}$/.test(password)) {
            newError.password = "パスワードは英数字混合で8〜16文字で入力してください。";
            isValid = false;
        }

        if (password !== confirmPassword) {
            newError.confirmPassword = "パスワードが一致しません。";
            isValid = false;
        }

        setError(newError);
        return isValid;
    };

    const handleRegister = async () => {
        if (!validateInputs()) return;

        try {
            await createUserWithEmailAndPassword(auth, email, password);
            console.log("現在のユーザー:", auth.currentUser);
            router.push("/individual/login/new/account"); 
        } catch (err) {
            console.error("登録エラー:", err);
            setError({ ...error, general: "アカウントの作成に失敗しました。" });
        }
    };

    return (
        <div>
            <BackButton />
            <form
                onSubmit={(e) => {
                    e.preventDefault();
                    handleRegister();
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
                    placeholder="パスワード（英数字混合8〜16文字）"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <InputField 
                    type="password" 
                    placeholder="パスワード確認"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
                <PrimaryButton type="submit">登録</PrimaryButton>
                {error.email && <p style={{ color: "red" }}>{error.email}</p>}
                {error.password && <p style={{ color: "red" }}>{error.password}</p>}
                {error.confirmPassword && <p style={{ color: "red" }}>{error.confirmPassword}</p>}
                {error.general && <p style={{ color: "red" }}>{error.general}</p>}
            </form>
        </div>
    );

}
