from datetime import datetime, timedelta

# Adjust inputs here
nsac = "NABC241" # NABC sanction name
start_date = datetime.strptime("2024-03-08", "%Y-%m-%d") # first Friday
end_date = datetime.strptime("2024-03-18", "%Y-%m-%d") # Monday after last Sunday

# Other parameters
base_url = "https://cdn.acbl.org/nabc/"
year_month = start_date.strftime("/%Y/%m/")
nsort_pre = int(nsac[4:]) * 100  # Extract numerical part and multiply by 100

# Pre-Bulletin INSERT
pre_bulletin = f"{base_url}{start_date.strftime('%Y/%m')}/bulletins/pre.pdf"
pre_bulletin_insert = f"""INSERT INTO db2.NABCFIL (NSANC, NSORT, NLINDSC, NRELEAS, LINK1, LINK1T, LINK1REL, LINK3REL, LINK4REL, LINK5REL, LINK6REL) VALUES ('{nsac}', {nsort_pre}, 'Pre-Bulletin', 'Y', '{pre_bulletin}', 'Bulletin', 'Y', 'N', 'N', 'N', 'N');"""

# Daily INSERTs
daily_inserts = []
current_date = start_date
db_counter = 1
while current_date <= end_date:
    nsort_daily = int(nsac[4:]) * 100 + db_counter
    date_desc = current_date.strftime("%a %b %-d")  # Format: Fri Oct 1
    daily_bulletin = f"{base_url}{current_date.strftime('%Y/%m')}/bulletins/db{db_counter}.pdf"
    
    insert_statement = f"""INSERT INTO db2.NABCFIL (NSANC, NSORT, NLINDSC, NRELEAS, LINK1, LINK1T, LINK1REL, LINK3REL, LINK4REL, LINK5REL, LINK6REL) VALUES ('{nsac}', {nsort_daily}, '{date_desc}', 'Y', '{daily_bulletin}', 'Bulletin', 'Y', 'N', 'N', 'N', 'N');"""
    
    daily_inserts.append(insert_statement)
    current_date += timedelta(days=1)
    db_counter += 1

# Combine all INSERT statements
all_inserts = [pre_bulletin_insert] + daily_inserts

# Output
print(*all_inserts, sep='\n')
