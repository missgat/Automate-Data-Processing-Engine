import os
import random
from datetime import datetime

# 1. Generator: Simulates a raw, messy user sign-up/sales log from a web app
def generate_raw_data(filename="raw_transactions.txt"):
    products = ["Premium_Subscription", "Basic_Tier", "Enterprise_License", "Add_On_Pack"]
    prices = {"Premium_Subscription": 49.99, "Basic_Tier": 19.99, "Enterprise_License": 299.99, "Add_On_Pack": 9.99}
    channels = ["Web_Store", "Mobile_App", "Referral", "Partner_API"]
    
    print(f"⚙️ Simulating raw transaction stream into '{filename}'...")
    with open(filename, "w",) as f:
        for _ in range(100):
            date_str = datetime.now().strftime("%Y-%m-%d")
            product = random.choice(products)
            price = prices[product]
            channel = random.choice(channels)
            user_id = f"USR-{random.randint(1000, 9999)}"
            
            # Write a raw string separated by custom delimiter (||)
            f.write(f"DATE:{date_str} || USER:{user_id} || ITEM:{product} || REVENUE:{price} || SOURCE:{channel}\n")
    print("✅ Raw transaction data generated.")

# 2. Analytics Engine: Reads, cleans, and processes the raw data stream
def process_data_stream(input_file="raw_transactions.txt", output_file="business_analytics_summary.txt"):
    if not os.path.exists(input_file):
        generate_raw_data(input_file)
        
    print(f"📊 Processing data from '{input_file}'...")
    
    total_revenue = 0.0
    transaction_count = 0
    item_popularity = {}
    channel_performance = {}

    # Open and process the file efficiently line by line
    with open(input_file, "r") as f:
        for line in f:
            if "||" in line:
                transaction_count += 1
                # Parse the key-value structures out of the text line
                segments = line.split(" || ")
                
                item = segments[2].split("ITEM:")[1].strip()
                revenue = float(segments[3].split("REVENUE:")[1].strip())
                source = segments[4].split("SOURCE:")[1].strip()
                
                # Accumulate business metrics
                total_revenue += revenue
                item_popularity[item] = item_popularity.get(item, 0) + 1
                channel_performance[source] = channel_performance.get(source, 0) + revenue

    # 3. Report Generation: Write structured business findings out to a new file
    print(f"📈 Generating Executive Business Report in '{output_file}'...")
    with open(output_file, "w", encoding="utf-8") as r:
        r.write("==================================================\n")
        r.write("💼 AUTOMATED DATA PROCESSING ENGINE REPORT       \n")
        r.write(f"Processed At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        r.write("==================================================\n\n")
        
        r.write("📊 HIGHLIGHT METRICS:\n")
        r.write("--------------------------------------------------\n")
        r.write(f"Total Processed Transactions: {transaction_count}\n")
        r.write(f"Total Gross Revenue: ${total_revenue:,.2f}\n")
        r.write(f"Average Order Value: ${total_revenue/transaction_count:,.2f}\n\n")
        
        r.write("📦 PRODUCT SALES VOLUME:\n")
        r.write("--------------------------------------------------\n")
        for item, count in sorted(item_popularity.items(), key=lambda x: x[1], reverse=True):
            r.write(f" - {item.replace('_', ' ')}: {count} units sold\n")
            
        r.write("\n🔌 REVENUE SHARE BY ACQUISITION CHANNEL:\n")
        r.write("--------------------------------------------------\n")
        for channel, rev in sorted(channel_performance.items(), key=lambda x: x[1], reverse=True):
            r.write(f" - {channel.replace('_', ' ')}: ${rev:,.2f} generated\n")

    print(f"🏁 Execution finished. Open '{output_file}' to review.")

if __name__ == "__main__":
    generate_raw_data()
    process_data_stream()
