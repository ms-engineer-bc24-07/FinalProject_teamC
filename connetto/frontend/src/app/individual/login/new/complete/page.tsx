"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import Image from "next/image";

export default function RegistrationComplete() {
  const router = useRouter();

    useEffect(() => {
        const timer = setTimeout(() => {
            router.push("/individual/participation");
        }, 2000);
    
        return () => clearTimeout(timer); 
    }, [router]);

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        marginTop: "200px",
        textAlign: "center",
      }}
    >
      <Image 
        src="/images/logo/complete.png" 
        alt="完了ロゴ" 
        width={100} 
        height={100} 
        style={{marginBottom: "30px" }}
      />
      <h1>登録が完了しました！</h1>
      <p>さっそく使い始めましょう</p>
    </div>
  );
}
