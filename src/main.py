from vulcan_predictor import VulcanPredictor
from vulcan_compliance import VulcanCompliance
import time

def run_vulcan_cycle():
    print("==========================================")
    print("   V.U.L.C.A.N. SYSTEM - ACTIVE MONITORING")
    print("==========================================\n")

    predictor = VulcanPredictor()
    compliance = VulcanCompliance(ac_tail_number="VT-VUL")

    # 1. Simulating real-time sensor ingestion
    print("[1/3] Ingesting Telemetry from Engine #1...")
    time.sleep(1)
    mock_telemetry = [680.2, 0.052, 44.8] # [EGT, Vibration, Pressure]

    # 2. Running AI Prediction
    print("[2/3] Analyzing Degradation Trends...")
    rul, health = predictor.predict_rul(mock_telemetry)
    print(f"      >> Health Index: {health:.2f}%")
    print(f"      >> Predicted RUL: {rul} Flight Cycles")

    # 3. Handling Maintenance Action
    if health < 85:
        print("\n[!] ALERT: PREDICTIVE THRESHOLD BREACHED")
        print("[3/3] Generating Maintenance Task Card...")
        card = compliance.generate_task_card("High-Pressure Turbine", rul)
        certified = compliance.certify_maintenance(card, "ENG-9902")
        print(f"      >> Task Card {certified['aircraft_id']} Created & Certified.")
        print("      >> System Status: COMPLIANT")
    else:
        print("\n[3/3] System Status: NOMINAL. No action required.")

    print("\n==========================================")

if __name__ == "__main__":
    run_vulcan_cycle()
