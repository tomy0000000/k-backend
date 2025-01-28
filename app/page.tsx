"use client";
import { Calendar } from "@/components/ui/calendar";
import React from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Separator } from "@/components/ui/separator";

const payments = [
  {
    title: "Payment 1",
    subtitle: "Wallet",
    amount: 100,
  },
  {
    title: "Payment 2",
    subtitle: "Credit Card",
    amount: -200,
  },
];

export default function CalendarApp() {
  const [date, setDate] = React.useState<Date | undefined>(new Date());

  return (
    <div className="flex h-full">
      <div>
        <Calendar
          mode="single"
          selected={date}
          onSelect={setDate}
          className="rounded-md border"
        />
      </div>

      <ScrollArea className="h-full w-full rounded-md">
        <hgroup className="p-4">
          <h1 className="text-lg font-semibold">Payments</h1>
          <h2 className="text-neutral-500">{date?.toLocaleDateString()}</h2>
        </hgroup>
        <div className="px-4">
          <Separator className="my-2" />
          {payments.map((payment) => (
            <>
              <div key={payment.title} className="text-sm">
                <div className="font-semibold">{payment.title}</div>
                <div className="text-neutral-500">{payment.subtitle}</div>
                <div className="text-sm">
                  {payment.amount > 0 ? "+" : "-"}${Math.abs(payment.amount)}
                </div>
              </div>
              <Separator className="my-2" />
            </>
          ))}
        </div>
      </ScrollArea>
    </div>
  );
}
