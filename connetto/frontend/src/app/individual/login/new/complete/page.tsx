"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function RegistrationComplete() {
  const router = useRouter();

  useEffect(() => {
    const timer = setTimeout(() => {
      router.push("/individual/participation/add");
    }, 2000);

    return () => clearTimeout(timer);
  }, [router]);

  return (
    <div>
      <div>
        <div>完了アイコン入れる</div>
      </div>
      <h1>登録が完了しました！</h1>
      <p>さっそく使い始めましょう</p>
    </div>
  );
}
