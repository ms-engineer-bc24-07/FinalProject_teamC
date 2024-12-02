"use client";

import { useRouter } from "next/navigation";
import BackButton from "@/components/BackButton/BackButton";
import InputField from "@/components/InputField/InputField";
import PrimaryButton from "@/components/PrimaryButton/PrimaryButton";

export default function Existing() {
  const router = useRouter();

  return (
    <div>
      <BackButton />
      <form>
        <InputField type="email" placeholder="メールアドレス" />
        <InputField type="password" placeholder="パスワード" />
      </form>
      <PrimaryButton>ログイン</PrimaryButton>
    </div>
  );
}
