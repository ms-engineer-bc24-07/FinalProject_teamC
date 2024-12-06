"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { collection, query, where, getDocs } from "firebase/firestore";
import { db } from "@/utils/firebase";
import InputField from "@/components/common/InputField/InputField";
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";
import BackButton from "@/components/common/BackButton/BackButton";

export default function CorporateLogin() {

    const router = useRouter();

    const [corporateCode, setCorporateCode] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    const handleNext = async () => {
        try {
            const q = query(
                collection(db, "companies"),
                where("corporateCode", "==", corporateCode)
            );
            const querySnapshot = await getDocs(q);

            if (!querySnapshot.empty) {
                const companyData = querySnapshot.docs[0].data();

                // パスワードを検証あとでハッシュ化すること（テスト用: プレーンテキスト）
                if (companyData.password === password) {
                    router.push("/individual/login/new/mail");
                } else {
                    setError("パスワードが正しくありません。");
                }
            } else {
                setError("企業コードが正しくありません。");
            }
        } catch (err) {
            console.error("Firestoreエラー:", err);
            setError("予期しないエラーが発生しました。");
        }
    };

    return (
        <div>
            <BackButton />
            <form onSubmit={(e) => e.preventDefault()}>
                <InputField 
                    type="text" 
                    placeholder="企業コード"
                    value={corporateCode}
                    onChange={(e) => setCorporateCode(e.target.value)}
                />
                <InputField 
                    type="password" 
                    placeholder="パスワード"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
            </form>
            {error && <p style={{ color: "red" }}>{error}</p>}
            <PrimaryButton onClick={handleNext}>次へ</PrimaryButton>
        </div>
    );

}

