"use client";

import { useRouter } from "next/navigation";
import BackButton from "@/components/common/BackButton/BackButton";
import InputField from "@/components/common/InputField/InputField";
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";

export default function Existing() {
  const router = useRouter();

<<<<<<< HEAD
  return (
    <div>
      <BackButton />
      <form>
        <InputField type="email" placeholder="メールアドレス" />
        <InputField type="password" placeholder="パスワード" />
      </form>
      <PrimaryButton>ログイン</PrimaryButton>
=======
    const navigateToHome = () => {
        router.push("/individual/participation"); 
    };

return (
    <div>
        <BackButton/>
        <form>
            <InputField type="email" placeholder="メールアドレス" />
            <InputField type="password" placeholder="パスワード" />
        </form>
            <PrimaryButton onClick={navigateToHome}>ログイン</PrimaryButton>
>>>>>>> 5145bb2f542abc4ed9b55ac015a3c271f31c99f1
    </div>
  );
}
