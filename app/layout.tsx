import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Cirrus",
  description: "Notice the thought and keep living.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
