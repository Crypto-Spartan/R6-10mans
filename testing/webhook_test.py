from discord import Webhook, AsyncWebhookAdapter
import aiohttp, asyncio
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rel_file_path = "conf/discord_webhook.txt"
abs_file_path = os.path.join(os.path.abspath(parent_dir), rel_file_path)

with open(abs_file_path, 'r') as f:
	discord_webhook_url = f.read()
	discord_webhook_url = discord_webhook_url.strip()


async def foo():
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(discord_webhook_url, adapter=AsyncWebhookAdapter(session))
        webhook_text = '''
        This is pretty cool.
        I think webhooks are awesome.
        probably gonna do it this way 
        '''
        await webhook.send(webhook_text, username='10-Mans Bot')

asyncio.run(foo())