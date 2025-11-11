from fastapi import Request
from fastapi.responses import JSONResponse

def json_error(message: str, status: int):
    return JSONResponse(status_code=status, content={"error": message})

async def unhandled_exception_handler(request: Request, exc: Exception):
    return json_error("internal error", 500)
