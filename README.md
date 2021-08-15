# Tesla Inventory Checker

Search Tesla Inventory API and Get Notified in Discord.

This attempts to replicate the same search performed on Tesla's website but without the heavy lifting of the assets and other elements that are loaded effectively making it easier on Tesla to return data to us and for us to get it quickly.

### Discord

Here's a temporary invite link to see this in action: https://discord.gg/2T8wZ25z

(Please message me if this expires and you would like to join)

### Instructions

1. Download & Install Python3 for your OS: https://www.python.org/downloads/
2. Clone this repository using your Git Client or download accordingly
3. Update `config.ini` file with your desired configuration
   - for lat_long, if you do not have that handy, you may comment out that line by placing `#` in the beginning of that line. The script will call Tesla API to get the Geolocation.
      ```
      #lat_long =
      ```
4. Run the python file in Terminal / Command Prompt with any customizations you want:
   ```bash
   // Example 1: with default config file and repeat option every 60 seconds
   python3 check_inventory.py -r 60

   // Example 2: with custom config file m3.ini and repeat option every 60 seconds
   python3 check_inventory.py -c m3.ini -r 60
   ```

For Discord API, create a webhook on your respective server/channel:

1. Open your Server Settings and head into the Integrations tab:
2. Click the "Create Webhook" button to create a new webhook!
3. Update `config.ini` with your webhook url
4. If you'd prefer to test your webhook, use `-dt` argument when running this script.

To be notified locally in Terminal (and not on Discord), use the `-l` or `-localonly` argument:
```bash
python3 check_inventory.py -r 60 -l
```

### Support

For any help or issues, feel free to reach out on Discord, Social Media: @NoorByDesign or over email: support@noorbydesign.com.

If you'd like to donate to this effort & buy me a coffee or something, it will be very much appreciated but not expected at all.

- Ko-Fi - https://ko-fi.com/tnoor
- Venmo/Cash - $TNOOR
