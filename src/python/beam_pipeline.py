import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
import risk_models_pb2 # Generated in Step 1
import CppRiskEngine   # Our compiled C++ module
import random
import os

# --- Data Generators ---
def generate_dummy_trades(count=100):
    trades = []
    counterparties = ["CPTY_A", "CPTY_B", "CPTY_C"]
    for i in range(count):
        req = risk_models_pb2.TradeRequest()
        req.trade_id = f"TRD_{i}"
        req.counterparty_id = random.choice(counterparties)
        req.trade_type = "OPTION"
        req.notional = 1000000
        req.strike = 100.0
        req.maturity = 1.0
        
        # Dummy Market Data
        req.spot_price = 100.0 + random.uniform(-10, 10)
        req.volatility = 0.20
        req.risk_free_rate = 0.05
        
        trades.append(req)
    return trades

# --- Beam DoFns ---

class CalculateRiskDoFn(beam.DoFn):
    """Wraps the C++ call"""
    def process(self, element):
        # element is a TradeRequest protobuf object
        # Serialize to bytes for C++
        req_bytes = element.SerializeToString()
        
        # Call C++ Binding
        resp_bytes = CppRiskEngine.calculate_risk(req_bytes)
        
        # Deserialize back to Python Protobuf
        result = risk_models_pb2.ValuationResult()
        result.ParseFromString(resp_bytes)
        
        # Key by Counterparty for aggregation
        yield (result.counterparty_id, result)

class AggregateRiskDoFn(beam.DoFn):
    """Aggregates risk per counterparty"""
    def process(self, element):
        cpty_id, results = element # (Key, List[ValuationResult])
        
        total_pv = sum(r.present_value for r in results)
        total_pfe = sum(r.pfe_95 for r in results)
        
        # Simple dummy CVA calculation
        cva = total_pfe * 0.02 
        
        agg_risk = risk_models_pb2.CounterpartyRisk()
        agg_risk.counterparty_id = cpty_id
        agg_risk.total_pv = total_pv
        agg_risk.total_pfe = total_pfe
        agg_risk.cva_charge = cva
        
        yield agg_risk

# --- The Pipeline ---

def run():
    options = PipelineOptions()
    
    trades = generate_dummy_trades(50)
    
    print("Starting Beam Pipeline...")
    
    with beam.Pipeline(options=options) as p:
        (
            p 
            | 'CreateTrades' >> beam.Create(trades)
            | 'Pricing(C++)' >> beam.ParDo(CalculateRiskDoFn())
            | 'GroupByKey'   >> beam.GroupByKey()
            | 'AggCCR'       >> beam.ParDo(AggregateRiskDoFn())
            | 'PrintResults' >> beam.Map(lambda x: print(f"Result: {x}"))
        )

if __name__ == '__main__':
    # Print the Process ID (PID) so you know which process to attach to
    print(f"Waiting for debugger. Process ID: {os.getpid()}")
    input("Press Enter to continue...")
    run()