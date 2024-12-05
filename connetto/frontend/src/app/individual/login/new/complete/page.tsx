"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function RegistrationComplete() {
  const router = useRouter();

<<<<<<< HEAD
  useEffect(() => {
    const timer = setTimeout(() => {
      router.push("/individual/participation/add");
    }, 2000);
=======
    useEffect(() => {
        const timer = setTimeout(() => {
            router.push("/individual/participation");
        }, 2000);
    
        return () => clearTimeout(timer); 
    }, [router]);
>>>>>>> 5145bb2f542abc4ed9b55ac015a3c271f31c99f1

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
