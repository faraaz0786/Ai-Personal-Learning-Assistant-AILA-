type SkeletonCardProps = {
  lines?: number;
};

export function SkeletonCard({ lines = 3 }: SkeletonCardProps) {
  return (
    <div className="animate-pulse rounded-2xl border border-neutral-200 bg-white p-6 shadow-sm">
      <div className="mb-4 h-5 w-1/3 rounded bg-neutral-200" />
      <div className="space-y-3">
        {Array.from({ length: lines }).map((_, index) => (
          <div
            key={index}
            className={`h-4 rounded bg-neutral-200 ${index === lines - 1 ? "w-2/3" : "w-full"}`}
          />
        ))}
      </div>
    </div>
  );
}
