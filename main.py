import flet as ft
import requests

def main(page: ft.Page):
    page.title = "Live Fibonacci Grid Matrix"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # UI Components for Displaying Data
    symbol_text = ft.Text("Symbol: XAUUSD", size=20, weight=ft.FontWeight.BOLD)
    ask_text = ft.Text("Live Ask: Loading...", size=24, color=ft.colors.GREEN_ACCENT, weight=ft.FontWeight.BOLD)
    ath_text = ft.Text("All-Time High: Loading...", size=16)
    
    # Grid container for the 5-layer blocks
    grid_column = ft.Column(scroll=ft.ScrollMode.AUTO, spacing=10)

    def fetch_and_calculate(e=None):
        try:
            # Fetching real-time market data feed (using a public financial API endpoint example)
            response = requests.get("https://api.coinbase.com/v2/prices/XAU-USD/spot", timeout=5)
            data = response.json()
            current_ask = float(data['data']['amount'])
            
            # Setting a baseline All-Time High reference (or pull dynamically from your preferred source library)
            all_time_high = current_ask * 1.15 

            ask_text.value = f"Live Ask: {current_ask:.2f}"
            ath_text.value = f"All-Time High Reference: {all_time_high:.2f}"

            # Calculate 5-Layer Fibonacci Blocks
            fib_ratios = [0.0, 0.236, 0.382, 0.50, 0.618, 1.0]
            price_span = all_time_high - current_ask
            
            grid_column.controls.clear()
            for i, ratio in enumerate(fib_ratios):
                layer_price = all_time_high - (price_span * ratio)
                
                # Dynamic coloring similar to your matrix layout
                bg_color = ft.colors.GREEN_900 if i % 2 == 0 else ft.colors.RED_900
                
                block = ft.Container(
                    content=ft.Text(f"Layer {i}: {layer_price:.2f}", size=16, weight=ft.FontWeight.BOLD),
                    bgcolor=bg_color,
                    padding=15,
                    border_radius=8,
                    alignment=ft.alignment.center
                )
                grid_column.controls.append(block)
            
            page.update()
        except Exception as ex:
            ask_text.value = "Error fetching live data"
            page.update()

    refresh_btn = ft.ElevatedButton("Refresh Matrix", on_click=fetch_and_calculate)

    page.add(
        symbol_text,
        ask_text,
        ath_text,
        ft.Divider(),
        refresh_btn,
        ft.Container(height=20),
        grid_column
    )

    # Initial load trigger
    fetch_and_calculate()

ft.app(target=main)
