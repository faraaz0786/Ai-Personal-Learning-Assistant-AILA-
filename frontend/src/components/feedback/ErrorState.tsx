import { Button } from "../atoms/Button";

type ErrorStateProps = {
  title?: string;
  message: string;
  onRetry?: () => void;
};

export function ErrorState({
  title = "Something went wrong",
  message,
  onRetry
}: ErrorStateProps) {
  return (
    <div className="rounded-2xl border border-error-500/20 bg-red-50 p-4 text-sm text-error-500">
      <p className="font-semibold">{title}</p>
      <p className="mt-1">{message}</p>
      {onRetry ? (
        <div className="mt-3">
          <Button variant="ghost" onClick={onRetry}>
            Retry
          </Button>
        </div>
      ) : null}
    </div>
  );
}
