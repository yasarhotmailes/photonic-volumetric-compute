"""
ITO (Indium Tin Oxide) layer controller for transparency management.
"""

import numpy as np
from typing import List, Dict, Tuple


class ITOController:
    """Controls ITO coating transparency via electrical signals."""
    
    def __init__(self, num_layers: int = 100):
        """Initialize ITO controller for a multi-layer stack."""
        self.num_layers = num_layers
        self.voltages: np.ndarray = np.zeros(num_layers)
        
        self.ito_properties = {
            "thickness_nm": 150.0,
            "sheet_resistance_ohms": 50.0,
            "transparency_threshold_v": 3.0,
            "transparency_at_0v": 0.95,
            "transparency_at_threshold": 0.5,
            "transparency_at_high_v": 0.01,
        }
        
        self.switching_time_ns = 1.0
        self.power_supply_v = 12.0
        self.current_per_layer_ua = 10.0
    
    def set_voltage(self, layer_id: int, voltage: float) -> None:
        """Set voltage for a specific layer."""
        if voltage < 0 or voltage > self.power_supply_v:
            raise ValueError(
                f"Voltage {voltage}V out of safe range [0, {self.power_supply_v}V]"
            )
        
        idx = layer_id - 1 if layer_id > 0 else layer_id
        
        if idx < 0 or idx >= self.num_layers:
            raise IndexError(f"Layer {layer_id} out of range [1, {self.num_layers}]")
        
        self.voltages[idx] = voltage
    
    def set_layer_pattern(self, active_layer: int) -> None:
        """Set voltage pattern to activate a single layer."""
        self.voltages.fill(0.0)
        self.set_voltage(active_layer, 5.0)
    
    def get_transparency(self, layer_id: int) -> float:
        """Get transparency factor for a layer (0=opaque, 1=transparent)."""
        idx = layer_id - 1
        voltage = self.voltages[idx]
        
        threshold = self.ito_properties["transparency_threshold_v"]
        
        if voltage < threshold:
            t_min = self.ito_properties["transparency_at_0v"]
            t_threshold = self.ito_properties["transparency_at_threshold"]
            progress = voltage / threshold
            return t_min - (t_min - t_threshold) * progress
        else:
            t_threshold = self.ito_properties["transparency_at_threshold"]
            t_max = self.ito_properties["transparency_at_high_v"]
            progress = (voltage - threshold) / (self.power_supply_v - threshold)
            return t_threshold - (t_threshold - t_max) * progress
    
    def get_all_transparencies(self) -> np.ndarray:
        """Get transparency factors for all layers."""
        transparencies = np.array([
            self.get_transparency(i + 1) for i in range(self.num_layers)
        ])
        return transparencies
    
    def calculate_power_consumption(self) -> float:
        """Calculate instantaneous power consumption for current voltage pattern."""
        total_current_a = 0.0
        
        for i in range(self.num_layers):
            voltage = self.voltages[i]
            sheet_resistance = self.ito_properties["sheet_resistance_ohms"]
            resistance = sheet_resistance * (1.0 + 0.1 * voltage)
            
            if resistance > 0:
                current = voltage / resistance
                total_current_a += current
        
        power_w = np.sum(self.voltages) * (total_current_a / self.num_layers)
        return max(0, power_w)
    
    def get_controller_info(self) -> dict:
        """Get comprehensive controller information."""
        return {
            "num_layers": self.num_layers,
            "current_voltages": self.voltages.tolist(),
            "current_transparencies": self.get_all_transparencies().tolist(),
            "power_consumption_w": self.calculate_power_consumption(),
            "switching_time_ns": self.switching_time_ns,
            "ito_properties": self.ito_properties,
            "max_voltage_v": self.power_supply_v,
        }
    
    def __repr__(self) -> str:
        """String representation of controller."""
        power_mw = self.calculate_power_consumption() * 1000
        return (
            f"ITOController({self.num_layers} layers, "
            f"power={power_mw:.2f}mW, "
            f"switching={self.switching_time_ns}ns)"
        )