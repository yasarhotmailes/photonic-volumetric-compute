"""
Single photonic glass layer model.
"""

import numpy as np
from typing import Tuple, Optional


class PhotonicLayer:
    """Represents a single layer in the photonic volumetric stack.
    
    A PhotonicLayer consists of:
    - Glass substrate: transparent structural layer
    - Weight matrix: phase modulation encoding model weights
    - ITO coating: electrically controllable transparency layer
    
    Attributes:
        layer_id (int): Layer identifier in stack (1-100)
        thickness_um (float): Layer thickness in micrometers
        pixel_resolution (Tuple[int, int]): Resolution (width, height) in pixels
        wavelength_nm (float): Operating wavelength in nanometers
        glass_refractive_index (float): Refractive index of glass substrate
        has_weights (bool): Whether this layer contains weight matrix
        has_ito (bool): Whether this layer has ITO coating
    """
    
    def __init__(
        self,
        layer_id: int,
        thickness_um: float = 2.5,
        pixel_resolution: Tuple[int, int] = (4096, 4096),
        wavelength_nm: float = 532.0,  # Green laser
        glass_refractive_index: float = 1.47,
        has_weights: bool = True,
        has_ito: bool = True,
    ):
        """Initialize a photonic layer.
        
        Args:
            layer_id: Unique identifier for layer (1-100)
            thickness_um: Glass thickness in micrometers
            pixel_resolution: Pixel grid resolution (width, height)
            wavelength_nm: Optical wavelength in nanometers
            glass_refractive_index: n value for glass at given wavelength
            has_weights: Whether layer contains weight matrix
            has_ito: Whether layer has ITO coating
        """
        self.layer_id = layer_id
        self.thickness_um = thickness_um
        self.pixel_resolution = pixel_resolution
        self.wavelength_nm = wavelength_nm
        self.glass_refractive_index = glass_refractive_index
        self.has_weights = has_weights
        self.has_ito = has_ito
        
        # Weight matrix (stored as phase mask 0-2π)
        self.phase_mask: Optional[np.ndarray] = None
        
        # ITO properties
        self.ito_thickness_nm = 150.0
        self.ito_voltage_applied = 0.0  # Volts
        self.ito_is_transparent = True
        
        # Optical properties
        self._calculate_optical_properties()
    
    def _calculate_optical_properties(self):
        """Calculate optical properties for this layer."""
        # Optical path length through glass
        self.optical_path_length = self.thickness_um * self.glass_refractive_index
        
        # Phase accumulation traveling through layer
        wavelength_um = self.wavelength_nm / 1000.0
        self.phase_accumulation = (2 * np.pi / wavelength_um) * self.optical_path_length
    
    def set_weight_matrix(self, weights: np.ndarray) -> None:
        """Set the weight matrix for this layer."""
        if weights.shape != self.pixel_resolution:
            raise ValueError(
                f"Weight matrix shape {weights.shape} doesn't match "
                f"pixel resolution {self.pixel_resolution}"
            )
        
        # Normalize weights to [0, 1] range
        weights_normalized = (weights - weights.min()) / (weights.max() - weights.min() + 1e-10)
        
        # Convert to phase mask [0, 2π]
        self.phase_mask = weights_normalized * 2 * np.pi
    
    def get_phase_modulation(self) -> np.ndarray:
        """Get the phase modulation pattern for this layer."""
        if self.phase_mask is None:
            return np.zeros(self.pixel_resolution)
        return self.phase_mask.copy()
    
    def apply_ito_voltage(self, voltage: float) -> None:
        """Apply voltage to ITO coating to control transparency."""
        self.ito_voltage_applied = voltage
        ito_threshold = 3.0
        self.ito_is_transparent = voltage < ito_threshold
    
    def get_ito_transparency(self) -> float:
        """Get current ITO transparency (0=opaque, 1=transparent)."""
        if not self.has_ito:
            return 1.0
        
        if self.ito_is_transparent:
            return 0.95
        else:
            return 0.01
    
    def get_layer_info(self) -> dict:
        """Get comprehensive information about this layer."""
        return {
            "layer_id": self.layer_id,
            "thickness_um": self.thickness_um,
            "pixel_resolution": self.pixel_resolution,
            "wavelength_nm": self.wavelength_nm,
            "has_weights": self.has_weights,
            "has_ito": self.has_ito,
            "ito_voltage_applied": self.ito_voltage_applied,
            "ito_is_transparent": self.ito_is_transparent,
            "ito_transparency_factor": self.get_ito_transparency(),
            "has_phase_mask": self.phase_mask is not None,
            "optical_path_length": self.optical_path_length,
            "phase_accumulation": self.phase_accumulation,
        }
    
    def __repr__(self) -> str:
        """String representation of layer."""
        transparency = "transparent" if self.ito_is_transparent else "opaque"
        weights = "with weights" if self.has_weights else "without weights"
        return (
            f"PhotonicLayer(id={self.layer_id}, thickness={self.thickness_um}μm, "
            f"{weights}, ITO={transparency})"
        )