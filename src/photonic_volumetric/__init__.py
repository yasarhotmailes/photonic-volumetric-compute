"""
Photonic Volumetric Computing Architecture

3D optical neural networks with non-volatile glass/ITO storage
for ultra-fast, energy-efficient AI inference.

Main Components:
  - core: Glass layer and stack management
  - optics: Optical physics and light propagation
  - neural: Neural network layer definitions
  - simulation: Simulation and benchmarking tools
  - hardware: Hardware specifications and modeling
"""

__version__ = "0.1.0"
__author__ = "Yasa Hotmail"
__license__ = "MIT"

# Import main classes for convenience
try:
    from photonic_volumetric.core import PhotonicLayer, PhotonicStack, ITOController
except ImportError:
    pass

__all__ = [
    "PhotonicLayer",
    "PhotonicStack",
    "ITOController",
]