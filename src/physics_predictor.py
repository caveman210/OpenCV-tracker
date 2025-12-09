import math

class PhysicsPredictor:
    def __init__(self,
                 gravity=9.8,
                 cor=0.65,
                 friction=0.02,
                 stop_speed=0.2,
                 dt=0.016):
        self.g = gravity
        self.cor = cor
        self.friction = friction
        self.stop_speed = stop_speed
        self.dt = dt

    def simulate(self, x, y, vx, vy, vz_initial=0.0, max_time=5.0):
        px = x
        py = y
        pz = 0.0
        vz = vz_initial
        trajectory = []
        bounce_count = 0
        max_heights = []
        peak_z = 0.0
        t = 0.0
        while t < max_time:
            t += self.dt
            vz -= self.g * self.dt
            pz += vz * self.dt
            peak_z = max(peak_z, pz)
            if pz <= 0.0:
                if vz < 0:
                    bounce_count += 1
                    max_heights.append(peak_z)
                    peak_z = 0.0
                    pz = 0.0
                    vz = -vz * self.cor
            px += vx * self.dt
            py += vy * self.dt
            speed = math.sqrt(vx * vx + vy * vy)
            if speed > 0:
                scale = max(0.0, 1.0 - self.friction)
                vx *= scale
                vy *= scale
            if speed < self.stop_speed and abs(vz) < self.stop_speed:
                break
            trajectory.append((px, py, pz))
        final_rest = (px, py)
        return trajectory, bounce_count, final_rest, max_heights
