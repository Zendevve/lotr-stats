import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Dúnedain Data Atlas | Tolkien History Through Data",
  description: "Explore the rulers, succession and political history of Númenor, Arnor and Gondor through reproducible data analysis by Zendevve.",
  other: {
    "codex-preview": "development",
  },
  icons: {
    icon: "/favicon.svg",
    shortcut: "/favicon.svg",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
