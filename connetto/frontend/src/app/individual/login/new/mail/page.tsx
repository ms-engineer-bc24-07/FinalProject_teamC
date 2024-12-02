"use client";

import { useRouter } from "next/navigation";
import InputField from "@/components/common/InputField/InputField";
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";
import BackButton from "@/components/common/BackButton/BackButton";

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
