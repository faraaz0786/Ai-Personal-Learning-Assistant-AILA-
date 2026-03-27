import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { Card } from "../molecules/Card";

interface AccuracyChartProps {
  data: Array<{ topic: string; score: number }>;
}

const COLORS = [
  "#6d5dfc", // Primary Violet
  "#8173ff", // Lighter Violet
  "#a299ff", // Softest Violet
  "#d6d2ff", // Pastel Violet
  "#e7e5e4", // Warm Stone
];

export function AccuracyChart({ data }: AccuracyChartProps) {
  return (
    <div className="h-[320px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e7e5e4" />
          <XAxis type="number" hide />
          <YAxis 
            dataKey="topic" 
            type="category" 
            axisLine={false}
            tickLine={false}
            tick={{ fill: "#64748b", fontSize: 11, fontWeight: 800 }}
            width={120}
          />
          <Tooltip
            cursor={{ fill: 'rgba(109, 93, 252, 0.05)' }}
            contentStyle={{
              backgroundColor: "#fff",
              border: "1px solid #e7e5e4",
              borderRadius: "20px",
              boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.05)",
              padding: "16px",
            }}
            labelStyle={{ color: "#1e293b", fontWeight: 800, marginBottom: "6px" }}
          />
          <Bar 
            dataKey="score" 
            radius={[0, 12, 12, 0]} 
            barSize={24}
            animationDuration={2000}
          >
            {data.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
