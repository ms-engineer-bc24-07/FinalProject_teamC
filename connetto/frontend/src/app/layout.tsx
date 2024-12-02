import type { Metadata } from "next";
import Header from "@/components/Header/Header";
import "@/styles/globals.css";

export const metadata: Metadata = {
  title: "Connetto",
  description: "社内のコミュニケーションの場を自動で設定",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>
        <Header />
        <main>{children}</main>
      </body>
    </html>
  );
}
