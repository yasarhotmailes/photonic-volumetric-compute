"""
100-layer photonic volumetric stack assembly.
"""

import numpy as np
from typing import List, Tuple, Optional
from photonic_volumetric.core.layer import PhotonicLayer


class PhotonicStack:
    """Assembly of multiple photonic layers forming the volumetric computing stack."""
    
    def __init__(
        self,
        num_layers: int = 100,
        layer_thickness_um: float = 2.5,
        pixel_resolution: Tuple[int, int] = (4096, 4096),
        wavelength_nm: float = 532.0,
        material: str = "glass",
        ito_coating: bool = True,
    ):
        """Initialize photonic stack."""
        self.num_layers = num_layers
        self.layer_thickness_um = layer_thickness_um
        self.pixel_resolution = pixel_resolution
        self.wavelength_nm = wavelength_nm
        self.material = material
        self.ito_coating = ito_coating
        
        # Set refractive index based on material
        self.glass_refractive_index = self._get_refractive_index()
        
        # Create layers
        self.layers: List[PhotonicLayer] = []
        self._create_layers()
        
        # Stack properties
        self.total_thickness_um = num_layers * layer_thickness_um
        self.total_height_mm = self.total_thickness_um / 1000.0
    
    def _get_refractive_index(self) -> float:
        """Get refractive index for chosen material at operating wavelength."""
        refractive_indices = {
            "glass": 1.47,
            "fused_silica": 1.46,
            "borosilicate": 1.47,
        }
        return refractive_indices.get(self.material, 1.47)
    
    def _create_layers(self) -> None:
        """Create all layers in the stack."""
        for i in range(1, self.num_layers + 1):
            has_weights = (i % 2 == 0)
            
            layer = PhotonicLayer(
                layer_id=i,
                thickness_um=self.layer_thickness_um,
                pixel_resolution=self.pixel_resolution,
                wavelength_nm=self.wavelength_nm,
                glass_refractive_index=self.glass_refractive_index,
                has_weights=has_weights,
                has_ito=self.ito_coating,
            )
            self.layers.append(layer)
    
    def get_layer(self, layer_id: int) -> PhotonicLayer:
        """Get a specific layer by ID."""
        if layer_id < 1 or layer_id > self.num_layers:
            raise IndexError(f"Layer {layer_id} out of range [1, {self.num_layers}]")
        return self.layers[layer_id - 1]
    
    def set_active_layer(self, layer_id: int) -> None:
        """Activate a specific layer by controlling ITO transparency."""
        for i, layer in enumerate(self.layers):
            if i + 1 == layer_id:
                layer.apply_ito_voltage(5.0)
            else:
                layer.apply_ito_voltage(0.0)
    
    def create_input_beam(self, intensity: float = 1.0) -> np.ndarray:
        """Create input light beam pattern."""
        x = np.linspace(-2, 2, self.pixel_resolution[0])
        y = np.linspace(-2, 2, self.pixel_resolution[1])
        X, Y = np.meshgrid(x, y)
        
        sigma = 0.5
        beam = np.exp(-(X**2 + Y**2) / (2 * sigma**2))
        
        return beam * intensity
    
    def measure_energy(self, num_photons: float = 1e9) -> float:
        """Estimate energy consumption for inference."""
        planck_constant = 6.626e-34
        speed_of_light = 3.0e8
        wavelength_m = self.wavelength_nm / 1e9
        
        energy_per_photon = planck_constant * speed_of_light / wavelength_m
        total_energy = num_photons * energy_per_photon
        
        switching_energy = self.num_layers * 100e-12
        
        return total_energy + switching_energy
    
    def get_stack_info(self) -> dict:
        """Get comprehensive information about the stack."""
        return {
            "num_layers": self.num_layers,
            "total_thickness_um": self.total_thickness_um,
            "total_height_mm": self.total_height_mm,
            "layer_thickness_um": self.layer_thickness_um,
            "pixel_resolution": self.pixel_resolution,
            "wavelength_nm": self.wavelength_nm,
            "material": self.material,
            "glass_refractive_index": self.glass_refractive_index,
            "ito_coating": self.ito_coating,
            "total_pixels_per_layer": self.pixel_resolution[0] * self.pixel_resolution[1],
            "total_parallel_channels": (
                self.num_layers * self.pixel_resolution[0] * self.pixel_resolution[1]
            ),
        }
    
    def __repr__(self) -> str:
        """String representation of stack."""
        return (
            f"PhotonicStack({self.num_layers} layers, "
            f"{self.total_thickness_um:.1f}μm total thickness, "
            f"{self.pixel_resolution[0]}x{self.pixel_resolution[1]} pixels/layer)"
        )