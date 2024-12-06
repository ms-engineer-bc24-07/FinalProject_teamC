import type { Metadata } from "next";
<<<<<<< HEAD
import Header from "@/components/Header/Header";
import "@/styles/globals.css";
=======
import Header from "@/components/layout/Header/Header";
import "@/styles/globals.css"
>>>>>>> 5145bb2f542abc4ed9b55ac015a3c271f31c99f1

export const metadata: Metadata = {
  title: "Connetto",
  description: "社内のコミュニケーションの場を自動で設定",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>
        <Header />
        <main style={{ marginTop: "60px", padding: "16px" }}>{children}</main>
      </body>
    </html>
  );
}
