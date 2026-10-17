import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routes import ApiError, router

app = FastAPI()
app.include_router(router)
logger = logging.getLogger(__name__)

@app.exception_handler(ApiError)
async def api_error_handler(request: Request, exc: ApiError):
    return JSONResponse(status_code=exc.status, content={"code": exc.code})

@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    first = exc.errors()[0]
    if first.get("loc", [None])[0] == "path": code = "id_invalid"
    elif request.method == "POST": code = "title_invalid"
    elif request.method == "PATCH": code = "completed_invalid"
    else: code = "http_error"
    return JSONResponse(status_code=422, content={"code": code})

@app.exception_handler(StarletteHTTPException)
async def http_error_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"code": "http_error"})

@app.exception_handler(Exception)
async def internal_error_handler(request: Request, exc: Exception):
    logger.exception("Unhandled application error", exc_info=exc)
    return JSONResponse(status_code=500, content={"code": "internal_error"})
