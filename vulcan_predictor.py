import numpy as np
import pandas as pd
import os

class VulcanPredictor:
    """
    AI Predictive Maintenance Engine.
    Uses degradation trending to estimate Remaining Useful Life (RUL).
    Industrial Grade: Incorporates EGT (Exhaust Gas Temp) and Vibration thresholds.
    """
    def __init__(self, data_path=None):
        self.data_path = data_path or os.path.join(os.path.dirname(__file__), '..', 'data', 'engine_sample.csv')
        self.egt_threshold = 750.0  # Celsius
        self.vibe_threshold = 0.08  # mm/s
        print("[VULCAN-BRAIN] Predictive Engine Initialized.")

    def load_historical_trends(self):
        """Loads historical degradation data to calibrate the model."""
        try:
            df = pd.read_csv(self.data_path)
            return df
        except Exception as e:
            print(f"[!] Error loading historical data: {e}")
            return None

    def estimate_rul(self, current_telemetry):
        """
        Estimates RUL based on current telemetry and degradation slopes.
        Telemetry format: [EGT, Vibration, Oil Pressure]
        """
        egt, vibe, press = current_telemetry
        
        # Calculate Health Index (0-100)
        # Weighting: EGT (50%), Vibration (30%), Pressure (20%)
        egt_score = max(0, 100 * (1 - (egt / self.egt_threshold)))
        vibe_score = max(0, 100 * (1 - (vibe / self.vibe_threshold)))
        press_score = min(100, press * 2) # Assume 50 psi is 100%
        
        health_index = (egt_score * 0.5) + (vibe_score * 0.3) + (press_score * 0.2)
        
        # Predict RUL: Simple linear degradation assumption for demo
        # Real LSTM would use sequence data, here we trend against health
        estimated_cycles = int(health_index * 2.8) 
        
        return estimated_cycles, health_index

    def run_diagnostics(self, current_telemetry):
        rul, health = self.estimate_rul(current_telemetry)
        print("\n" + "="*40)
        print("   VULCAN PREDICTIVE HEALTH REPORT")
        print("="*40)
        print(f"Current Health Index: {health:.2f}%")
        print(f"Estimated RUL:       {rul} Cycles")
        print("-" * 40)
        
        if health < 85:
            print("[!] ALERT: Maintenance Action Recommended.")
        else:
            print("[✓] Status: Engine Healthy.")
        print("="*40 + "\n")
        return rul, health

if __name__ == "__main__":
    predictor = VulcanPredictor()
    # Mock data: Increasing EGT and Vibration
    mock_flight_data = [
        [620.0, 0.012, 48.0],
        [680.5, 0.045, 45.2],
        [735.0, 0.075, 42.1]
    ]
    
    for i, data in enumerate(mock_flight_data):
        print(f"Analyzing Flight Cycle {i+1}...")
        predictor.run_diagnostics(data)
