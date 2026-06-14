"use client";

import { useEffect, useRef } from "react";

export function ThreeDBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationId: number;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);

    // GSAP Brand Theme Colors
    const colors = [
      "rgba(136, 206, 2, ",   // GSAP Neon Green
      "rgba(52, 211, 153, ",  // Emerald/Mint Green
      "rgba(226, 232, 240, ",  // Silver/Gray
      "rgba(138, 192, 7, ",   // Lime Green
    ];

    type Particle = {
      id: string;
      x: number;
      y: number;
      z: number;
      vx: number;
      vy: number;
      vz: number;
      colorPrefix: string;
      baseAlpha: number;
      radius: number;
      age: number;
      life: number;
      parentId: string | null;
      growth: number; // 0 to 1 branching animation progress
    };

    let particles: Particle[] = [];
    const maxParticles = 45;

    const createParticle = (parent?: Particle): Particle => {
      const id = Math.random().toString(36).substring(2, 9);
      const colorPrefix = colors[Math.floor(Math.random() * colors.length)];
      const baseAlpha = colorPrefix.includes("136") ? 0.4 : 0.3;
      const radius = Math.random() * 3 + 2;

      let life = Math.floor(Math.random() * 200) + 200; // 200 to 400 frames for root

      let x = (Math.random() - 0.5) * 800;
      let y = (Math.random() - 0.5) * 800;
      let z = Math.random() * 800 + 200;

      // Drift speed
      let vx = (Math.random() - 0.5) * 0.3;
      let vy = (Math.random() - 0.5) * 0.3;
      let vz = (Math.random() - 0.5) * 0.15;

      let parentId: string | null = null;

      if (parent) {
        parentId = parent.id;
        const parentRemaining = parent.life - parent.age;
        // Child life is capped at a fraction of parent remaining life to die first
        life = Math.floor(Math.random() * (parentRemaining * 0.75)) + 40;
        if (life >= parentRemaining) {
          life = Math.max(30, parentRemaining - 10);
        }

        // Spawn near parent to form a branch
        const angle = Math.random() * Math.PI * 2;
        const dist = Math.random() * 60 + 30;
        x = parent.x + Math.cos(angle) * dist;
        y = parent.y + Math.sin(angle) * dist;
        z = parent.z + (Math.random() - 0.5) * 40;

        // Share velocity closely so the bond structure stays cohesive
        vx = parent.vx + (Math.random() - 0.5) * 0.04;
        vy = parent.vy + (Math.random() - 0.5) * 0.04;
        vz = parent.vz + (Math.random() - 0.5) * 0.02;
      }

      return {
        id,
        x,
        y,
        z,
        vx,
        vy,
        vz,
        colorPrefix,
        baseAlpha,
        radius,
        age: 0,
        life,
        parentId,
        growth: 0,
      };
    };

    // Populate initial batch as connected trees
    for (let i = 0; i < 30; i++) {
      if (particles.length > 0 && Math.random() < 0.85) {
        const parent = particles[Math.floor(Math.random() * particles.length)];
        particles.push(createParticle(parent));
      } else {
        particles.push(createParticle());
      }
    }

    let cx = width / 2;
    let cy = height / 2;

    const handleResize = () => {
      if (!canvas) return;
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
      cx = width / 2;
      cy = height / 2;
    };

    window.addEventListener("resize", handleResize);

    const fov = 380; // Perspective projection factor

    const animate = () => {
      ctx.clearRect(0, 0, width, height);

      // Y-axis 3D camera rotation angle
      const angle = 0.0003;
      const cos = Math.cos(angle);
      const sin = Math.sin(angle);

      // Spawning new branches dynamically
      if (particles.length < maxParticles && Math.random() < 0.08) {
        const parent = particles.length > 0 ? particles[Math.floor(Math.random() * particles.length)] : undefined;
        particles.push(createParticle(parent));
      }

      // Map of particles by ID for quick parent lookup
      const particleMap = new Map<string, Particle>();
      particles.forEach((p) => particleMap.set(p.id, p));

      // Update and filter particles
      particles = particles.filter((p) => {
        p.age++;
        if (p.age >= p.life) return false; // Destroy

        // 3D camera sweep rotation
        const rx = p.x * cos - p.z * sin;
        const rz = p.z * cos + p.x * sin;
        p.x = rx;
        p.z = rz;

        // Apply drift speed
        p.x += p.vx;
        p.y += p.vy;
        p.z += p.vz;

        // Repulsive snap-off drift force during decay phase
        if (p.parentId) {
          const parent = particleMap.get(p.parentId);
          if (parent) {
            const childDecay = p.life - p.age <= 60 ? (60 - (p.life - p.age)) / 60 : 0;
            const parentDecay = parent.life - parent.age <= 60 ? (60 - (parent.life - parent.age)) / 60 : 0;
            const decayProgress = Math.max(childDecay, parentDecay);

            if (decayProgress > 0) {
              const dx = p.x - parent.x;
              const dy = p.y - parent.y;
              const dz = p.z - parent.z;
              const len = Math.sqrt(dx * dx + dy * dy + dz * dz) || 1;
              const pushForce = 0.25 * decayProgress; // Slowly accelerate away
              p.x += (dx / len) * pushForce;
              p.y += (dy / len) * pushForce;
              p.z += (dz / len) * pushForce;
            }
          }
        }

        // Boundary bounce controls
        if (Math.abs(p.x) > 450) p.vx *= -1;
        if (Math.abs(p.y) > 450) p.vy *= -1;
        if (p.z < 150 || p.z > 950) p.vz *= -1;

        // Branch growth increment
        if (p.parentId && p.growth < 1) {
          p.growth += 0.025; // Reaches 1 in 40 frames
          if (p.growth > 1) p.growth = 1;
        }

        return true;
      });

      // Update map after filtering
      particleMap.clear();
      particles.forEach((p) => particleMap.set(p.id, p));

      // Draw branching lines (parent-child connections)
      particles.forEach((p) => {
        if (!p.parentId || p.z <= 0) return;
        const parent = particleMap.get(p.parentId);
        if (!parent || parent.z <= 0) return;

        // Calculate decay progress
        const childDecay = p.life - p.age <= 60 ? (60 - (p.life - p.age)) / 60 : 0;
        const parentDecay = parent.life - parent.age <= 60 ? (60 - (parent.life - parent.age)) / 60 : 0;
        const decayProgress = Math.max(childDecay, parentDecay);

        // Calculate line alpha (fade-in on spawn, fade-out on decay)
        let lineAlpha = 0.25; // High visibility baseline
        if (p.age < 40) {
          lineAlpha *= (p.age / 40);
        }
        if (decayProgress > 0) {
          lineAlpha *= (1 - decayProgress);
        }

        const scale1 = fov / p.z;
        const scale2 = fov / parent.z;

        const x1 = cx + p.x * scale1;
        const y1 = cy + p.y * scale1;
        const x2 = cx + parent.x * scale2;
        const y2 = cy + parent.y * scale2;

        // Grow line towards parent
        const targetX = x1 + (x2 - x1) * p.growth;
        const targetY = y1 + (y2 - y1) * p.growth;

        // Apply dashed breakdown logic
        if (decayProgress > 0) {
          const dashLength = Math.max(0.5, 6 * (1 - decayProgress));
          const gapLength = 2 + 14 * decayProgress;
          ctx.setLineDash([dashLength, gapLength]);
        } else {
          ctx.setLineDash([]);
        }

        ctx.strokeStyle = `rgba(136, 206, 2, ${lineAlpha})`;
        ctx.lineWidth = 0.65 * scale1;
        ctx.beginPath();
        ctx.moveTo(x1, y1);
        ctx.lineTo(targetX, targetY);
        ctx.stroke();
      });

      // Reset line dash
      ctx.setLineDash([]);

      // Render nodes (atoms)
      particles.forEach((p) => {
        if (p.z <= 0) return;

        // Calculate opacity based on age and decay
        let alpha = 0.7; // baseline opacity for atoms
        if (p.age < 40) {
          alpha = 0.7 * (p.age / 40);
        } else if (p.age > p.life - 40) {
          alpha = 0.7 * ((p.life - p.age) / 40);
        }

        const scale = fov / p.z;
        const screenX = cx + p.x * scale;
        const screenY = cy + p.y * scale;

        if (screenX >= 0 && screenX <= width && screenY >= 0 && screenY <= height) {
          // Sharp, tiny atomic junction scaled by depth
          const radius = Math.max(1.0, Math.min(3.0, 1.4 * scale));

          // Draw small solid core
          ctx.beginPath();
          ctx.arc(screenX, screenY, radius, 0, Math.PI * 2);
          ctx.fillStyle = `${p.colorPrefix}${alpha})`;
          ctx.fill();
        }
      });

      animationId = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener("resize", handleResize);
    };
  }, []);

  return <canvas ref={canvasRef} className="canvas-3d" />;
}
