"use client";

import React from "react";
import styles from "./Header.module.css";
import { usePathname } from "next/navigation";
import Image from "next/image";

export default function Header() {
  const pathname = usePathname();
  const hideHeader = pathname === "/";

  if (hideHeader) return null;

  return (
    <header className={styles.header}>
        <Image 
          src="/images/logo/title_logo.png" 
          alt="タイトルロゴ" 
          width={190} 
          height={55} 
          style={{marginBottom: "3px" }}
        />
    </header>
  );
}
