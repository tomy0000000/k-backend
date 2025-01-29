"use client"
import { Calendar } from "@/components/ui/calendar"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Separator } from "@/components/ui/separator"
import { useToast } from "@/hooks/use-toast"
import { PaymentReadDetailed, readPaymentsPaymentsGet } from "@/lib/client"
import { useAuth } from "@/lib/context/AuthContext"
import { useEffect, useState } from "react"

export default function CalendarApp() {
  const { client } = useAuth()
  const { toast } = useToast()
  const [date, setDate] = useState<Date | undefined>(new Date())
  const [loading, setLoading] = useState(true)
  const [payments, setPayments] = useState<PaymentReadDetailed[]>([])

  useEffect(() => {
    if (!client) {
      return
    }

    setLoading(true)
    const payment_date = date?.toLocaleDateString("en-CA") // 2025-01-01

    async function fetchPayments() {
      const response = await readPaymentsPaymentsGet({
        client,
        query: { payment_date },
      })
      if (response.error) {
        throw new Error("Failed to fetch payments")
      }
      if (!response.data) {
        throw new Error("No data returned")
      }
      setPayments(response.data)
    }

    try {
      fetchPayments()
    } catch (error) {
      console.error(error)
      toast({
        title: "Failed to fetch payments",
        description:
          error instanceof Error ? error.message : "An unknown error occurred",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }, [date, client, toast])

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
        <hgroup className="p-4 pb-0">
          <h1 className="text-lg font-semibold">Payments</h1>
          <h2 className="text-neutral-500">{date?.toLocaleDateString()}</h2>
        </hgroup>
        <div className="px-4">
          <Separator className="my-2" />
          {loading && (
            <p className="tex-sm text-center text-neutral-500 leading-10">
              Loading...
            </p>
          )}
          {payments.length === 0 && (
            <p className="tex-sm text-center text-neutral-500 leading-10">
              No payments
            </p>
          )}
          {payments.map((payment) => {
            const total = Number(payment.total)
            return (
              <div key={payment.id}>
                <div className="flex flex-row justify-between text-sm">
                  <div className="flex flex-col">
                    <div className="font-semibold">{payment.description}</div>
                    <div className="text-neutral-500">
                      {payment.description}
                    </div>
                  </div>
                  <div className="flex items-center justify-center bg-red-500 text-white px-4 py-2 rounded-md">
                    {payment.type === "Expense" && `-${total}`}
                    {payment.type === "Income" && `+${total}`}
                  </div>
                </div>
                <Separator className="my-2" />
              </div>
            )
          })}
        </div>
      </ScrollArea>
    </div>
  )
}
