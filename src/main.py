from telethon import TelegramClient
import pandas as pd
import asyncio

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

channels = ['@channel1', '@channel2', '@channel3']

async def main():
    client = TelegramClient('session', api_id, api_hash)
    await client.start()
    
    all_data = []
    
    for channel in channels:
        print(f"Crawling {channel}...")
        messages = []
        
        async for message in client.iter_messages(channel, limit=5000):
            if message.text:
                messages.append({
                    'channel': channel,
                    'message_id': message.id,
                    'date': message.date,
                    'text': message.text,
                    'views': message.views
                })
        
        all_data.extend(messages)
        await asyncio.sleep(2)  # Rate limiting
    
    df = pd.DataFrame(all_data)
    df.to_csv('telegram_crawled_data.csv', index=False)
    print(f"Extracted {len(df)} messages")
    
    await client.disconnect()

if __name__ == '__main__':
    asyncio.run(main())
