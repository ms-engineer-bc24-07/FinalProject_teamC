"use client";

import { useRouter } from "next/navigation";
import InputField from "@/components/InputField/InputField";
import PrimaryButton from "@/components/PrimaryButton/PrimaryButton";
import BackButton from "@/components/BackButton/BackButton";

export default function CorporateLogin() {
    const router = useRouter()

    const navigateToMail = () => {
        router.push("/individual/login/new/mail"); 
    };

    return (
        <div>
            <BackButton />
            <form>
                <InputField type="code" placeholder="企業コード" />
                <InputField type="password" placeholder="パスワード" />
            </form>
            <PrimaryButton onClick={navigateToMail}>次へ</PrimaryButton>

        </div>
    );
}
