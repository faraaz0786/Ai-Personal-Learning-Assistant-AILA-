import { Card } from "./Card";
import { ReactNode } from "react";
import { ArrowUpRight } from "lucide-react";

type FeatureCardProps = {
  title: string;
  description: string;
  icon: ReactNode;
};

export function FeatureCard({ title, description, icon }: FeatureCardProps) {
  return (
    <Card 
      className="group/feature hover:-translate-y-1 transition-all duration-300 relative"
      noPadding
    >
      <div className="p-8 md:p-10 space-y-6">
        <div className="w-12 h-12 rounded-2xl bg-primary-50 flex items-center justify-center text-primary-600 border border-primary-100 shadow-sm group-hover/feature:bg-primary-600 group-hover/feature:text-white transition-colors duration-300">
          {icon}
        </div>
        
        <div className="space-y-3">
          <h3 className="text-xl font-black text-slate-800 tracking-tight flex items-center justify-between">
            {title}
            <ArrowUpRight className="text-slate-300 group-hover/feature:text-primary-500 transition-colors" size={20} />
          </h3>
          <p className="text-slate-500 font-medium leading-relaxed">
            {description}
          </p>
        </div>
      </div>
    </Card>
  );
}
