"""
Personal Finance Tracker API - Main application.

A FastAPI-based REST API for tracking personal financial transactions.

Follows API-specific conventions from src/CLAUDE.md:
- Async route handlers
- FastAPI HTTPException for errors
- Python logging module
- Pydantic response models
- Single quotes for dictionary keys

Documentation available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
"""

import logging
import sys
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from .router import router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title='Personal Finance Tracker API',
    description='A REST API for managing personal financial transactions with categories, amounts, and descriptions',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc'
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Include transaction router
app.include_router(router)

logger.info('FastAPI application initialized')


@app.get(
    '/health',
    status_code=status.HTTP_200_OK,
    summary='Health check',
    description='Check API health and version information'
)
async def health_check() -> dict:
    """
    Health check endpoint.

    Returns:
        Dictionary with status and version (using single quotes per API convention)
    """
    return {
        'status': 'healthy',
        'service': 'Personal Finance Tracker API',
        'version': '1.0.0'
    }


@app.get(
    '/',
    status_code=status.HTTP_200_OK,
    summary='API root',
    description='Get API information and available endpoints'
)
async def root() -> dict:
    """
    Root endpoint with API information.

    Returns:
        Dictionary with API details and documentation links
    """
    return {
        'message': 'Personal Finance Tracker API',
        'version': '1.0.0',
        'documentation': {
            'swagger_ui': '/docs',
            'redoc': '/redoc'
        },
        'endpoints': {
            'health': '/health',
            'transactions': '/api/v1/transactions'
        }
    }


if __name__ == '__main__':
    import uvicorn

    logger.info('Starting development server')

    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
        log_level='info'
    )
