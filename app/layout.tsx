"use client";
import React from "react";
import { cn } from "@/lib/utils";
import "./globals.css";
import AppSidebar from "@/components/app-sidebar";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`antialiased`}>
        <div
          className={cn(
            "rounded-md flex flex-col md:flex-row bg-gray-100 dark:bg-neutral-800 w-full flex-1 overflow-hidden h-screen"
          )}
        >
          <AppSidebar />
          <div className="container mx-auto bg-white h-full p-4">
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}
