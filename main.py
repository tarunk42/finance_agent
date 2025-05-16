# # main.py (top-level)
# from api import app

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("finance_agents.api:app", host="0.0.0.0", port=5050, reload=True)


import os
from api import app
import uvicorn

if __name__ == "__main__":
    # Use the PORT environment variable set by Render
    port = int(os.environ.get("PORT", 10000))  # 10000 is default; fallback is for local dev
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=False)
