"use client";

import React, { useEffect, useRef } from "react";

interface OrbProps {
    isActive: boolean;
    isTalking: boolean;
    volume: number; // 0 to 1
}

export default function Orb({ isActive, isTalking, volume }: OrbProps) {
    const canvasRef = useRef<HTMLCanvasElement>(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        if (!canvas) return;

        const ctx = canvas.getContext("2d");
        if (!ctx) return;

        let animationFrameId: number;
        let time = 0;

        const render = () => {
            time += 0.05;

            // Resize canvas to match display size
            const { width, height } = canvas.getBoundingClientRect();
            if (canvas.width !== width || canvas.height !== height) {
                canvas.width = width;
                canvas.height = height;
            }

            const centerX = width / 2;
            const centerY = height / 2;

            // Clear
            ctx.clearRect(0, 0, width, height);

            if (!isActive) {
                // Dormant state: faint small circle
                ctx.beginPath();
                ctx.arc(centerX, centerY, 50, 0, Math.PI * 2);
                ctx.fillStyle = "rgba(255, 255, 255, 0.1)";
                ctx.fill();
                return;
            }

            // Active State
            // Base radius pulses slightly
            const baseRadius = 100 + Math.sin(time) * 5;

            // Volume reaction
            const volumeScale = 1 + volume * 0.5; // Scale up to 1.5x
            const currentRadius = baseRadius * volumeScale;

            // Glow Gradient
            const gradient = ctx.createRadialGradient(centerX, centerY, currentRadius * 0.2, centerX, centerY, currentRadius * 2);

            if (isTalking) {
                // AI Talking: Blue/Purple/White
                gradient.addColorStop(0, "rgba(255, 255, 255, 1)");
                gradient.addColorStop(0.4, "rgba(100, 200, 255, 0.5)");
                gradient.addColorStop(1, "rgba(0, 0, 0, 0)");
            } else {
                // Listening/Thinking: White/Gold
                gradient.addColorStop(0, "rgba(255, 255, 255, 1)");
                gradient.addColorStop(0.4, "rgba(255, 255, 200, 0.3)");
                gradient.addColorStop(1, "rgba(0, 0, 0, 0)");
            }

            // Draw Orb
            ctx.beginPath();
            ctx.arc(centerX, centerY, currentRadius * 2, 0, Math.PI * 2);
            ctx.fillStyle = gradient;
            ctx.fill();

            // Inner Core
            ctx.beginPath();
            ctx.arc(centerX, centerY, currentRadius * 0.4, 0, Math.PI * 2);
            ctx.fillStyle = "rgba(255, 255, 255, 0.9)";
            ctx.fill();

            animationFrameId = requestAnimationFrame(render);
        };

        render();

        return () => {
            cancelAnimationFrame(animationFrameId);
        };
    }, [isActive, isTalking, volume]);

    return (
        <canvas
            ref={canvasRef}
            className="w-full h-full absolute inset-0 pointer-events-none"
        />
    );
}
