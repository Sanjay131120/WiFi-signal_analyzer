import subprocess
import re
import pandas as pd
import matplotlib.pyplot as plt
import time

def get_wifi_data():
    command_output = subprocess.run(['netsh', 'wlan', 'show', 'network', 'mode=bssid'], capture_output=True, text=True)
    output_text = command_output.stdout

    pattern = r'\bSSID (\d+) : (.+?)\n.*?Signal\s+:\s+(\d+)%'
    matches = re.findall(pattern, output_text, re.DOTALL)

    data = {'SSID': [], 'Signal_Strength': []}
    for ssid, ssid_name, signal_strength in matches:
        data['SSID'].append(ssid_name)
        data['Signal_Strength'].append(int(signal_strength))

    return pd.DataFrame(data)

def main():
    while True:
        df = get_wifi_data()

        plt.figure(figsize=(10, 6))
        plt.scatter(df.index, df['Signal_Strength'], c=df['Signal_Strength'], cmap='viridis', s=df['Signal_Strength']*10)
        plt.colorbar(label='Signal Strength (%)')
        plt.xticks(df.index, df['SSID'], rotation=45, ha='right')
        plt.xlabel('SSID')
        plt.ylabel('Signal Strength (%)')
        plt.title('WiFi Signal Strength Heat Map')
        plt.tight_layout()
        plt.show()

        max_signal_row = df.loc[df['Signal_Strength'].idxmax()]
        print(f"Suggesting network to connect: {max_signal_row['SSID']} with signal strength {max_signal_row['Signal_Strength']}%")

        time.sleep(30)

if __name__ == "__main__":
    main()
