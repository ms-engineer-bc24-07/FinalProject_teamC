"use client";

import { useRouter } from "next/navigation";
import PrimaryButton from "@/components/common/PrimaryButton/PrimaryButton";
import Image from "next/image";

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
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          justifyContent: "center",
          alignItems: "center",
          height: "200px", 
          marginTop: "200px",
          textAlign: "center",
        }}
      >
        <Image 
          src="/images/logo/logo.png" 
          alt="ロゴ" 
          width={50} 
          height={50} 
          style={{marginBottom: "30px" }}
        />
        <Image 
          src="/images/title/title.png" 
          alt="タイトル" 
          width={200} 
          height={30}
        />
      </div>
      <div style={{ marginTop: "75px" }}>
        <PrimaryButton onClick={navigateToLogin}>ログイン</PrimaryButton>
        <PrimaryButton onClick={navigateToRegister}>新規登録</PrimaryButton>
      </div>
    </div>
  );
}
