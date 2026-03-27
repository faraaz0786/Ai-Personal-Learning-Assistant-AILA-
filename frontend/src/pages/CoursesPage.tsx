import { GraduationCap } from "lucide-react";
import { Button } from "../components/atoms/Button";
import { Link } from "react-router-dom";

export function CoursesPage() {
  return (
    <div className="flex flex-col items-center justify-center h-full space-y-8 p-12 text-center">
      <div className="w-20 h-20 rounded-3xl bg-primary-100 flex items-center justify-center shadow-academic">
        <GraduationCap className="text-primary-600" size={40} />
      </div>
      <div className="max-w-md space-y-4">
        <h1 className="text-3xl font-editorial font-bold text-surface-text-primary">Curriculum Vitae</h1>
        <p className="text-secondary-muted font-serif">
          Structured academic pathways and certified courses are being drafted by our mentor council. 
          Your formal education journey will commence shortly.
        </p>
      </div>
      <Link to="/learn">
        <Button variant="primary" className="rounded-xl px-8 py-3">
          Return to Study
        </Button>
      </Link>
    </div>
  );
}
