# Live Market Watch - Setup Guide (Hinglish)

Ye ek live NSE stock price website hai jo Dhan API se data leti hai
aur browser mein real-time update karti hai (WebSocket se).

## Files kya hain
- `app.py` - main backend code (Dhan se data laata hai)
- `templates/index.html` - website ka page
- `static/style.css` - design
- `static/script.js` - live update wala logic
- `requirements.txt` - jo Python packages chahiye
- `Procfile` - hosting ke liye instruction

## Step 1: Dhan API details bharo
`app.py` file kholo (Notepad ya Sublime Text se bhi khol sakte ho),
in 2 lines mein apna Client ID aur Access Token daalo:

```
DHAN_CLIENT_ID = os.environ.get("DHAN_CLIENT_ID", "YOUR_CLIENT_ID_HERE")
DHAN_ACCESS_TOKEN = os.environ.get("DHAN_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN_HERE")
```
`YOUR_CLIENT_ID_HERE` ki jagah apna asli Client ID daalo, waise hi Access Token.

Agar aur stocks add/remove karne hain to `WATCHLIST` list mein
Dhan ke master CSV se symbol ka `securityId` dhundh ke add kar do.

## Step 2: Website ko internet pe live karna (bina VS Code/terminal ke)

1. **GitHub par account banao** (agar nahi hai) - github.com
2. Is poori `stock-site` folder ko ek naye GitHub repository mein
   **upload karo** (GitHub website pe hi "Add file → Upload files"
   button se, drag-and-drop kar sakte ho - koi code editor nahi chahiye)
3. **Render.com** par jao, free account banao
4. "New +" → "Web Service" → apna GitHub repo select karo
5. Render khud detect kar lega ki ye Python app hai. Bas confirm karo:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: (Procfile se khud le lega)
6. "Environment" section mein apni Dhan keys bhi daal sakte ho
   (zyada safe rahega code mein daalne se):
   - `DHAN_CLIENT_ID`
   - `DHAN_ACCESS_TOKEN`
7. "Create Web Service" dabao - Render 2-3 minute mein site live kar dega
   aur tumhe ek link dega jaise: `https://your-site-name.onrender.com`

Bas! Ye link kisi ko bhi bhejo, wo browser mein khol ke live prices dekh
sakta hai - unhe koi file download nahi karni.

## Baad mein update karna ho to
GitHub website pe hi file edit karo (pencil icon) aur save karo -
Render khud naya version deploy kar dega. Code editor kabhi nahi
kholna padega.

## Note
Dhan API ka commercial/public redistribution wala terms of service
zaroor check kar lena, kyunki ye public site hogi (sirf apne use ke
liye nahi).
