import type React from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { TrendingUp, TrendingDown } from "lucide-react"

interface StatsCardProps {
  title: string
  value: number | string
  description: string
  trend: number
  trendDirection?: "up" | "down"
  icon?: React.ReactNode
  isCurrency?: boolean
  isPercentage?: boolean
  trendLabel?: string
}

export function StatsCard({
  title,
  value,
  description,
  trend,
  trendDirection = "up",
  icon,
  isCurrency = false,
  isPercentage = false,
  trendLabel = "from last period",
}: StatsCardProps) {
  const formattedValue =
    typeof value === "number"
      ? isCurrency
        ? new Intl.NumberFormat("en-IN", {
            style: "currency",
            currency: "INR",
            maximumFractionDigits: 0,
          }).format(value)
        : isPercentage
          ? `${value}%`
          : value.toLocaleString()
      : value

  const actualTrendDirection = trendDirection === "down" ? (trend > 0 ? "down" : "up") : trend > 0 ? "up" : "down"
  const trendColor = actualTrendDirection === "up" ? "text-green-600" : "text-red-600"

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold">{formattedValue}</div>
        <CardDescription className="flex items-center gap-1">
          {description}
          <div className={`ml-auto flex items-center gap-1 ${trendColor}`}>
            {actualTrendDirection === "up" ? <TrendingUp className="h-3 w-3" /> : <TrendingDown className="h-3 w-3" />}
            <span className="text-xs">{Math.abs(trend)}%</span>
            <span className="text-xs text-muted-foreground">{trendLabel}</span>
          </div>
        </CardDescription>
      </CardContent>
    </Card>
  )
}
