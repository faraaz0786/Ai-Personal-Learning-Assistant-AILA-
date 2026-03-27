import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Area,
  AreaChart,
} from "recharts";
import { Card } from "../molecules/Card";

interface PerformanceChartProps {
  data: Array<{ date: string; score: number }>;
}

export function PerformanceChart({ data }: PerformanceChartProps) {
  // Format dates for display (e.g., "Oct 12")
  const formattedData = data.map((item) => ({
    ...item,
    displayDate: new Date(item.date).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
    }),
  }));

  return (
    <div className="h-[320px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={formattedData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6d5dfc" stopOpacity={0.15} />
              <stop offset="95%" stopColor="#6d5dfc" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e7e5e4" />
          <XAxis 
            dataKey="displayDate" 
            axisLine={false}
            tickLine={false}
            tick={{ fill: "#94a3b8", fontSize: 11, fontWeight: 700 }}
            dy={15}
          />
          <YAxis 
            axisLine={false}
            tickLine={false}
            tick={{ fill: "#94a3b8", fontSize: 11, fontWeight: 700 }}
            domain={[0, 100]}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: "#fff",
              border: "1px solid #e7e5e4",
              borderRadius: "20px",
              boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.05)",
              padding: "16px",
            }}
            itemStyle={{ color: "#6d5dfc", fontWeight: 800 }}
            labelStyle={{ color: "#64748b", marginBottom: "6px", fontSize: "12px", fontWeight: 700 }}
          />
          <Area
            type="monotone"
            dataKey="score"
            stroke="#6d5dfc"
            strokeWidth={4}
            fillOpacity={1}
            fill="url(#colorScore)"
            animationDuration={2000}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
