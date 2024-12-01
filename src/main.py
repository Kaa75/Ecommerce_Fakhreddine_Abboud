"""
Main entry point for the Ecommerce API.
Initializes the FastAPI app, middleware, and routes.
"""

import os
import sys

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from src.auth.router import auth_router
from src.config import Config
from src.controllers import (
    customers_router,
    inventory_router,
    review_router,
    sales_router,
    status_router,
)

# Add the project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

app = FastAPI(
    title=Config.APP.TITLE,
    description=Config.APP.DESCRIPTION,
    version=Config.APP.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(inventory_router)
app.include_router(review_router)
app.include_router(customers_router)
app.include_router(status_router)
app.include_router(auth_router)
app.include_router(sales_router)


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    """
    Serve the welcome HTML page for the Ecommerce API.

    Returns:
        HTMLResponse: The HTML content with welcome message and links to documentation.
    """
    html_content = """
    <html>
        <head>
            <title>Ecommerce Abboud Fakhreddine 435L</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h1 {
                    color: #333;
                }
                p {
                    color: #666;
                }
                a {
                    color: #06f;
                }
            </style>
        </head>
        <body>
            <h1>Welcome to the Ecommerce Karim Abboud Rayan Fakhreddine 435L API</h1>
            <p>To access the docs, visit <a href="/docs">docs</a> or <a href="/redoc">redoc</a></p>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=status.HTTP_200_OK)
