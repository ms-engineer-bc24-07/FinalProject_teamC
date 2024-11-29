"use client";

import { useRouter } from "next/navigation";
import InputField from "@/components/InputField/InputField";
import PrimaryButton from "@/components/PrimaryButton/PrimaryButton";
import BackButton from "@/components/BackButton/BackButton";

export default function MailRegister() {
    const router = useRouter()

    const navigateToVerify = () => {
        router.push("/individual/login/new/verify"); 
    };

    return (
        <div>
            <BackButton />
            <form>
                <InputField type="email" placeholder="メールアドレス" />
            </form>
            <PrimaryButton onClick={navigateToVerify}>認証コードを送信</PrimaryButton>
        </div>
    );
}
