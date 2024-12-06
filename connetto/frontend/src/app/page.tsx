"use client";

import { useRouter } from "next/navigation";
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";

export default function Home() {
  const router = useRouter();

  const navigateToLogin = () => {
    router.push("/individual/login/existing");
  };

  const navigateToRegister = () => {
    router.push("/individual/login/new");
  };

  return (
    <div>
      <PrimaryButton onClick={navigateToLogin}>ログイン</PrimaryButton>
      <PrimaryButton onClick={navigateToRegister}>新規登録</PrimaryButton>
    </div>
  );
}
