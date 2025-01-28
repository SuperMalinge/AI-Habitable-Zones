import math
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class Star:
    def __init__(self, luminosity, mass, temperature, age, activity, galaxy, metallicity=1.0, 
                 magnetic_field=1.0, rotation_period=25, spectral_class="G"):
        self.luminosity = luminosity
        self.mass = mass
        self.temperature = temperature
        self.age = age
        self.activity = activity
        self.galaxy = galaxy
        self.metallicity = metallicity
        self.magnetic_field = magnetic_field
        self.rotation_period = rotation_period
        self.spectral_class = spectral_class

class Planet:
    def __init__(self, name, orbital_distance, radius, mass, atmosphere, gravity, eccentricity,
                 magnetic_field=0.0, water_content=0.0, surface_temp=0, rotation_period=24,
                 axial_tilt=23.5, geological_activity=0.5):
        self.name = name
        self.orbital_distance = orbital_distance
        self.radius = radius
        self.mass = mass
        self.atmosphere = atmosphere
        self.gravity = gravity
        self.eccentricity = eccentricity
        self.magnetic_field = magnetic_field
        self.water_content = water_content
        self.surface_temp = surface_temp
        self.rotation_period = rotation_period
        self.axial_tilt = axial_tilt
        self.geological_activity = geological_activity

def calculate_habitable_zone(star):
    metallicity_factor = 1 + (star.metallicity - 1) * 0.05
    magnetic_factor = 1 + star.magnetic_field * 0.1
    rotation_factor = 1 + (star.rotation_period - 25) * 0.01
    
    base_inner = math.sqrt(star.luminosity/1.1)
    base_outer = math.sqrt(star.luminosity/0.53)
    
    age_factor = 1 + (star.age - 4.6) * 0.1
    activity_factor = 1 - star.activity * 0.2
    
    inner_bound = base_inner * age_factor * activity_factor * metallicity_factor * magnetic_factor * rotation_factor
    outer_bound = base_outer * age_factor * activity_factor * metallicity_factor * magnetic_factor * rotation_factor
    
    return inner_bound, outer_bound

def is_potentially_habitable(planet, inner_bound, outer_bound):
    effective_distance = planet.orbital_distance * (1 - planet.eccentricity**2)**0.25
    basic_zone_check = inner_bound <= effective_distance <= outer_bound
    
    atmosphere_check = bool(planet.atmosphere)
    mass_check = 0.1 <= planet.mass <= 10
    gravity_check = 5 <= planet.gravity <= 15
    magnetic_check = planet.magnetic_field >= 0.1
    water_check = planet.water_content > 0
    temperature_check = -50 <= planet.surface_temp <= 50
    rotation_check = 10 <= planet.rotation_period <= 40
    tilt_check = 10 <= planet.axial_tilt <= 45
    geological_check = planet.geological_activity > 0.2
    
    return all([
        basic_zone_check, atmosphere_check, mass_check, gravity_check,
        magnetic_check, water_check, temperature_check, rotation_check,
        tilt_check, geological_check
    ])

class HabitableZoneGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Habitable Zone Finder")
        
        self.input_frame = ttk.Frame(root, padding="10")
        self.input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.plot_frame = ttk.Frame(root, padding="10")
        self.plot_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.setup_inputs()
        self.setup_plot()
        self.update_visualization()

    def setup_inputs(self):
        self.star = Star(
            luminosity=1.0, mass=1.0, temperature=5778, age=4.6,
            activity=0.2, galaxy="Milky Way", metallicity=1.0,
            magnetic_field=1.0, rotation_period=25, spectral_class="G"
        )
        
        self.planets = [
            Planet("Earth", 1.0, 1.0, 1.0, {"N2": 0.78, "O2": 0.21}, 9.81, 0.017,
                  magnetic_field=1.0, water_content=0.7, surface_temp=15,
                  rotation_period=24, axial_tilt=23.5, geological_activity=0.6),
            Planet("Mars", 1.524, 0.532, 0.107, {"CO2": 0.95}, 3.72, 0.094,
                  magnetic_field=0.01, water_content=0.001, surface_temp=-63,
                  rotation_period=24.6, axial_tilt=25.2, geological_activity=0.1),
            Planet("Venus", 0.723, 0.949, 0.815, {"CO2": 0.96}, 8.87, 0.007,
                  magnetic_field=0.001, water_content=0.0, surface_temp=462,
                  rotation_period=243, axial_tilt=177.3, geological_activity=0.7),
            Planet("Kepler-442b", 0.409, 1.34, 2.34, {"Unknown": 1}, 11.2, 0.04,
                  magnetic_field=0.8, water_content=0.5, surface_temp=10,
                  rotation_period=30, axial_tilt=20, geological_activity=0.5)
        ]

    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
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
            self.ax.plot(x, y, '--', color='green', alpha=0.8)
        
        # Fill habitable zone
        r = np.linspace(inner_bound, outer_bound, 100)
        theta = np.linspace(0, 2*np.pi, 100)
        r, theta = np.meshgrid(r, theta)
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        self.ax.fill(x.flatten(), y.flatten(), alpha=0.2, color='green')
        
        # Plot star
        self.ax.plot(0, 0, 'yo', markersize=20, label=f'{self.star.spectral_class}-type Star')
        
        # Plot planets with orbital paths
        for planet in self.planets:
            # Plot orbital path
            orbit_theta = np.linspace(0, 2*np.pi, 100)
            orbit_x = planet.orbital_distance * np.cos(orbit_theta)
            orbit_y = planet.orbital_distance * np.sin(orbit_theta)
            self.ax.plot(orbit_x, orbit_y, '--', color='gray', alpha=0.3)
            
            # Plot planet
            x = planet.orbital_distance * np.cos(0)
            y = planet.orbital_distance * np.sin(0)
            color = 'blue' if is_potentially_habitable(planet, inner_bound, outer_bound) else 'red'
            self.ax.plot(x, y, 'o', color=color, markersize=10,
                        label=f'{planet.name} ({planet.mass:.1f} M⊕)')
        
        self.ax.set_aspect('equal')
        self.ax.legend(loc='upper right')
        self.ax.set_title(f'Habitable Zone Analysis in {self.star.galaxy}')
        self.ax.set_xlabel('Distance (AU)')
        self.ax.set_ylabel('Distance (AU)')
        self.ax.grid(True, alpha=0.3)
        
        self.canvas.draw()

def main():
    root = tk.Tk()
    app = HabitableZoneGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
