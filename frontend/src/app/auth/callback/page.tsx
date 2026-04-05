"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { supabase } from "@/lib/supabase";

export default function AuthCallbackPage() {
  const router = useRouter();

  useEffect(() => {
    const handleAuthCallback = async () => {
      const { error } = await supabase.auth.getSession();
      if (error) {
        console.error("Error during auth callback:", error.message);
      }
      // Redirect to home after processing
      router.push("/");
    };

    handleAuthCallback();
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#f8f9fc]">
      <div className="text-center">
        <div
          className="w-12 h-12 border-4 border-[#059669] border-t-transparent rounded-full mx-auto mb-6"
          style={{ animation: "spin 1s linear infinite" }}
        />
        <h2 className="text-xl font-bold text-[#1a1d2b] mb-2 font-outfit">
          Autenticando...
        </h2>
        <p className="text-sm text-[#5f6577]">
          Quase lá! Estamos preparando sua experiência.
        </p>
      </div>
      <style jsx>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        .font-outfit { font-family: var(--font-outfit); }
      `}</style>
    </div>
  );
}
