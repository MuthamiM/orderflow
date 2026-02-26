# Local Setup Guide (Free)

For the Hackathon demo, the fastest and 100% free way to run this project is completely locally on your machine, using `ngrok` to expose your local Python server to the internet so that n8n can send it webhooks.

## 1. Start the Python Execution Engine
1. Open up a terminal.
2. `cd engine`
3. Activate the virtual environment: `.\venv\Scripts\Activate.ps1`
4. Make sure your `.env` file is filled out with your API keys.
5. Boot the server: `python main.py`

Your server is now running on `http://localhost:8000`.

## 2. Expose the Server with ngrok
Because n8n might be running in the cloud or in a separate container, it needs a public URL to talk to your local Python server.
1. Open a **second, new terminal**.
2. Run `ngrok http 8000`
3. Ngrok will give you a "Forwarding" secure URL that looks like `https://xyz123.ngrok-free.app`

## 3. Run the n8n Workflow
1. Start your local n8n instance by running `npx n8n` in a **third terminal**.
2. Go to `http://localhost:5678` in your browser.
3. Import the `n8n/polymarket_arbitrage_workflow.json` file.
4. **Crucial Step:** Open the final "HTTP Request" node. Change the URL from `http://localhost:8000/api/v1/trade` to your new ngrok forwarding URL you got in step 2: `https://xyz123.ngrok-free.app/api/v1/trade`.

You are now fully live and trading without needing to pay for Render! Make sure to take a video recording of this process for your Devpost submission!
