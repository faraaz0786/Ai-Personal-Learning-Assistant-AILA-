import { useState, useEffect } from "react";
import { motion } from "framer-motion";

type TypewriterTextProps = {
  text: string;
  speed?: number;
  className?: string;
  delay?: number;
  onComplete?: () => void;
};

export function TypewriterText({
  text,
  speed = 20,
  className = "",
  delay = 0,
  onComplete
}: TypewriterTextProps) {
  const [displayedText, setDisplayedText] = useState("");
  const [started, setStarted] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => {
      setStarted(true);
    }, delay);
    return () => clearTimeout(timer);
  }, [delay]);

  useEffect(() => {
    if (!started) return;

    if (displayedText.length < text.length) {
      const nextChar = text[displayedText.length];
      const timer = setTimeout(() => {
        setDisplayedText((prev) => prev + nextChar);
      }, speed);
      return () => clearTimeout(timer);
    } else if (onComplete) {
      onComplete();
    }
  }, [displayedText, text, speed, started, onComplete]);

  return (
    <span className={className}>
      {displayedText}
      {displayedText.length < text.length && (
        <motion.span
          animate={{ opacity: [1, 0] }}
          transition={{ repeat: Infinity, duration: 0.8 }}
          className="inline-block w-1.5 h-5 ml-1 bg-primary-500 align-middle"
        />
      )}
    </span>
  );
}
