import type { Metadata } from "next";
import Header from "@/components/layout/Header/Header";
import "@/styles/globals.css"

export const metadata: Metadata = {
  title: "Connetto",
  description: "社内のコミュニケーションの場を自動で設定",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>
        <Header />
        <main style={{ marginTop: "60px", padding: "16px" }}>{children}</main>
      </body>
    </html>
  );
}
