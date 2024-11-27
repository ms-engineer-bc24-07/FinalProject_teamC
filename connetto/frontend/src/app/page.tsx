"use client";

import { useRouter } from "next/navigation";

export default function Home() {
  const router = useRouter()

  const navigateToLogin = () => {
    router.push("/individual/login"); 
  };

  const navigateToRegister = () => {
    router.push("/individual/register"); 
  };

  return (
    <div>
      <div>
        <button onClick={navigateToLogin}>
          ログイン
        </button>
        <button onClick={navigateToRegister}>
          新規登録
        </button>
      </div>
    </div>
  );
}
