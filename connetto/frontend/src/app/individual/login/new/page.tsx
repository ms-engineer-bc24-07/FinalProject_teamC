"use client";

import { useRouter } from "next/navigation";
import InputField from "@/components/common/InputField/InputField";
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";
import BackButton from "@/components/common/BackButton/BackButton";

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
