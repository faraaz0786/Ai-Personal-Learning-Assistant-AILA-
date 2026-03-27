import { ReactNode } from "react";
import { Link } from "react-router-dom";

import { Button } from "../atoms/Button";

type EmptyStateProps = {
  title: string;
  description: string;
  actionLabel?: string;
  actionTo?: string;
  icon?: ReactNode;
};

export function EmptyState({
  title,
  description,
  actionLabel,
  actionTo,
  icon
}: EmptyStateProps) {
  return (
    <div className="rounded-3xl border border-dashed border-neutral-200 bg-white/80 p-8 text-center shadow-sm">
      <div className="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-2xl bg-neutral-50 text-primary-600">
        {icon ?? <span className="text-xl font-bold">A</span>}
      </div>
      <h2 className="text-xl font-semibold text-neutral-900">{title}</h2>
      <p className="mx-auto mt-2 max-w-xl text-sm text-neutral-700">{description}</p>
      {actionLabel && actionTo ? (
        <Link to={actionTo} className="mt-6 inline-block">
          <Button>{actionLabel}</Button>
        </Link>
      ) : null}
    </div>
  );
}
