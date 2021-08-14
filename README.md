# Tesla Inventory Checker

Search Tesla Inventory API and Get Notified in Discord

Here's a temporary invite link to see this in action: https://discord.gg/2T8wZ25z

### Instructions

1. Download & Install Python3 for your OS: https://www.python.org/downloads/
2. Clone this repository using your Git Client or download accordingly
3. Update `config.ini` file with your desired configuration
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

If you need any help, feel free to reach out on Discord, Social Media: @NoorByDesign or over email: support@noorbydesign.com
