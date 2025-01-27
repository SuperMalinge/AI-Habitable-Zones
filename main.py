import math
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Star:
    def __init__(self, luminosity, mass, temperature, age, activity, galaxy):
        self.luminosity = luminosity
        self.mass = mass
        self.temperature = temperature
        self.age = age  # in billion years
        self.activity = activity  # 0-1 scale
        self.galaxy = galaxy

class Planet:
    def __init__(self, name, orbital_distance, radius, mass, atmosphere, gravity, eccentricity):
        self.name = name
        self.orbital_distance = orbital_distance
        self.radius = radius
        self.mass = mass  # in Earth masses
        self.atmosphere = atmosphere  # dict of composition
        self.gravity = gravity  # in m/s²
        self.eccentricity = eccentricity

def calculate_habitable_zone(star):
    # Enhanced calculation including stellar age and activity
    base_inner = math.sqrt(star.luminosity/1.1)
    base_outer = math.sqrt(star.luminosity/0.53)
    
    # Adjust for stellar age and activity
    age_factor = 1 + (star.age - 4.6) * 0.1  # Reference: Sun's age
    activity_factor = 1 - star.activity * 0.2
    
    inner_bound = base_inner * age_factor * activity_factor
    outer_bound = base_outer * age_factor * activity_factor
    
    return inner_bound, outer_bound

def is_potentially_habitable(planet, inner_bound, outer_bound):
    # Enhanced habitability check
    effective_distance = planet.orbital_distance * (1 - planet.eccentricity**2)**0.25
    basic_zone_check = inner_bound <= effective_distance <= outer_bound
    
    # Additional checks
    atmosphere_check = bool(planet.atmosphere)  # Must have atmosphere
    mass_check = 0.1 <= planet.mass <= 10  # Earth masses range
    gravity_check = 5 <= planet.gravity <= 15  # m/s² range
    
    return all([basic_zone_check, atmosphere_check, mass_check, gravity_check])

class HabitableZoneGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Habitable Zone Finder")
        
        # Create main frames
        self.input_frame = ttk.Frame(root, padding="10")
        self.input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.plot_frame = ttk.Frame(root, padding="10")
        self.plot_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.setup_inputs()
        self.setup_plot()
        self.update_visualization()

    def setup_inputs(self):
        # Star inputs
        ttk.Label(self.input_frame, text="Star Properties").grid(column=0, row=0)
        self.star = Star(1.0, 1.0, 5778, 4.6, 0.2, "Milky Way")
        
        # Planet list
        self.planets = [
            Planet("Earth", 1.0, 1.0, 1.0, {"N2": 0.78, "O2": 0.21}, 9.81, 0.017),
            Planet("Mars", 1.524, 0.532, 0.107, {"CO2": 0.95}, 3.72, 0.094),
            Planet("Venus", 0.723, 0.949, 0.815, {"CO2": 0.96}, 8.87, 0.007),
            Planet("Kepler-442b", 0.409, 1.34, 2.34, {"Unknown": 1}, 11.2, 0.04)
        ]

    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().grid(column=0, row=0)

    def update_visualization(self):
        self.ax.clear()
        inner_bound, outer_bound = calculate_habitable_zone(self.star)
        
        # Plot habitable zone
        theta = np.linspace(0, 2*np.pi, 100)
        for r in [inner_bound, outer_bound]:
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            self.ax.plot(x, y, '--', color='green')
        
        # Fill habitable zone
        r = np.linspace(inner_bound, outer_bound, 100)
        theta = np.linspace(0, 2*np.pi, 100)
        r, theta = np.meshgrid(r, theta)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        self.ax.fill(x.flatten(), y.flatten(), alpha=0.3, color='green')
        
        # Plot star
        self.ax.plot(0, 0, 'yo', markersize=15, label='Star')
        
        # Plot planets
        for planet in self.planets:
            x = planet.orbital_distance * np.cos(0)
            y = planet.orbital_distance * np.sin(0)
            color = 'blue' if is_potentially_habitable(planet, inner_bound, outer_bound) else 'red'
            self.ax.plot(x, y, 'o', color=color, label=planet.name)
        
        self.ax.set_aspect('equal')
        self.ax.legend()
        self.ax.set_title(f'Habitable Zone in {self.star.galaxy}')
        self.ax.set_xlabel('Distance (AU)')
        self.ax.set_ylabel('Distance (AU)')
        
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = HabitableZoneGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
