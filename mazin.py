import MetaTrader5 as mt5
import pandas as pd

# 1. Initialize Connection to MT5 Terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

def calculate_fib_grid_layers(symbol: str):
    # Ensure symbol is available in Market Watch
    symbol_info = mt5.symbol_info(symbol)
    if symbol_info is None:
        print(f"Symbol {symbol} not found.")
        return None
    
    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            print(f"Failed to select {symbol}")
            return None

    # 2. Fetch all-time or long-term historical data (e.g., Daily timeframe 'D1')
    # copy_rates_from_pos grabs bars starting from index 0 (current) going back
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_D1, 0, 1000)
    if rates is None or len(rates) == 0:
        print(f"Failed to retrieve historical rates for {symbol}")
        return None

    df = pd.DataFrame(rates)
    
    # 3. Automatically isolate the All-Time High (ATH) from the historical library
    all_time_high = df['high'].max()
    
    # 4. Get current live ask price
    tick = mt5.symbol_info_tick(symbol)
    current_ask = tick.ask if tick else df['close'].iloc[-1]

    # 5. Calculate 5-Layer Proportional / Fibonacci-style blocks
    # Using standard retracement or custom step multipliers derived from the ATH
    fib_ratios = [0.0, 0.236, 0.382, 0.50, 0.618, 1.0]
    
    layers = []
    price_span = all_time_high - current_ask
    
    for ratio in fib_ratios:
        # Dynamic block calculation per layer
        layer_price = all_time_high - (price_span * ratio)
        layers.append(round(layer_price, 2))

    # Output the structured matrix block
    matrix_data = {
        "Symbol": symbol,
        "Live Ask": current_ask,
        "All-Time High": all_time_high,
        "Layer Blocks (5-Step Matrix)": layers
    }
    
    return matrix_data

# Example Execution for XAUUSD
target_symbol = "XAUUSD"
result = calculate_fib_grid_layers(target_symbol)

if result:
    print(f"--- Matrix Generated for {result['Symbol']} ---")
    print(f"Live Ask Price : {result['Live Ask']}")
    print(f"All-Time High  : {result['All-Time High']}")
    print(f"Calculated 5-Layer Blocks: {result['Layer Blocks (5-Step Matrix)']}")

# Shut down connection
mt5.shutdown()
