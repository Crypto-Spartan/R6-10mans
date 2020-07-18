from discord import Webhook, AsyncWebhookAdapter
import aiohttp, asyncio

async def foo():
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url('https://discordapp.com/api/webhooks/728913048890507264/kaDijgGtC9wKfGKY_R2kLvZWgFf9TQyhbjZa-rj6FIUfxqSdyyZk_dY2_fN8fMnZYrjd', adapter=AsyncWebhookAdapter(session))
        webhook_text = '''
        This is pretty cool.
        I think webhooks are awesome.
        probably gonna do it this way 
        '''
        await webhook.send(webhook_text, username='Foo')

asyncio.run(foo())