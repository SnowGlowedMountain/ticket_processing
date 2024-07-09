import uvicorn
import os
from app.settings import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="localhost",
        port=settings.port,
        reload=True,
        log_level="info",
    )

