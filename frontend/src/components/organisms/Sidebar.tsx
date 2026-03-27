import { Link, useLocation } from "react-router-dom";
import { 
  Home, 
  BookText, 
  GraduationCap, 
  Settings,
  Brain
} from "lucide-react";
import { useUserStore } from "../../store/userStore";

const NAV_ITEMS = [
  { name: "Home", path: "/", icon: Home },
  { name: "Library", path: "/library", icon: BookText },
  { name: "AI Tutor", path: "/learn", icon: Brain },
  { name: "Courses", path: "/courses", icon: GraduationCap, status: "COMING SOON" },
];

export function Sidebar() {
  const location = useLocation();
  const balance = useUserStore((state) => state.balance);

  return (
    <aside className="hidden lg:flex flex-col w-64 h-screen sticky top-0 left-0 bg-background-alt border-r border-surface-border shrink-0 z-40">
      <div className="p-8">
        <Link to="/" className="flex items-center gap-3 group">
          <div className="w-10 h-10 rounded-xl bg-primary-500 flex items-center justify-center shadow-academic transform group-hover:rotate-3 transition-transform duration-300">
            <Brain className="text-white" size={20} />
          </div>
          <div className="flex flex-col">
            <span className="text-xl font-editorial font-bold text-surface-text-primary tracking-tight leading-none">AILA</span>
            <span className="text-[10px] text-primary-500 font-bold uppercase tracking-widest mt-1">AI Tutor</span>
          </div>
        </Link>
      </div>

      <nav className="flex-1 px-4 space-y-2">
        {NAV_ITEMS.map((item) => {
          const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));
          const isDisabled = item.status === "COMING SOON";
          
          return (
            <Link 
              key={item.path} 
              to={isDisabled ? "#" : item.path}
              className={`scholarly-sidebar-link ${isActive ? 'scholarly-sidebar-link-active' : ''} ${isDisabled ? 'opacity-50 cursor-not-allowed pointer-events-none' : ''}`}
              onClick={(e) => isDisabled && e.preventDefault()}
            >
              <div className="flex items-center gap-3 flex-1">
                <item.icon size={20} strokeWidth={isActive ? 2.5 : 2} className={isActive ? 'text-primary-500' : 'text-surface-text-secondary'} />
                <span className={isActive ? 'font-bold' : 'font-medium'}>{item.name}</span>
              </div>
              {isDisabled && (
                <span className="text-[8px] font-bold bg-background-alt px-1.5 py-0.5 rounded text-secondary-muted border border-surface-border">SOON</span>
              )}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 mt-auto">
        <div className="p-4 rounded-xl bg-white/50 border border-surface-border mb-4">
          <p className="text-xs text-secondary-muted font-medium mb-2">SCHOLAR BALANCE</p>
          <div className="flex items-center justify-between">
            <span className="text-lg font-editorial font-bold text-surface-text-primary">{balance.toLocaleString()} <span className="text-xs text-secondary-muted italic">pts</span></span>
            <div className="w-2 h-2 rounded-full bg-primary-500 animate-pulse" />
          </div>
        </div>
        
        <button className="w-full scholarly-sidebar-link group">
          <Settings size={20} className="text-surface-text-secondary group-hover:rotate-45 transition-transform duration-500" />
          <span className="font-medium">Settings</span>
        </button>
      </div>
    </aside>
  );
}
