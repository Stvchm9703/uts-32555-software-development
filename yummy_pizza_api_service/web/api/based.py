
from pydantic import BaseModel
from typing import Optional, Any

from fastapi import status


class Message(BaseModel):
    edited: Optional[Any] = None
    reason: Optional[str]
    status: Optional[str]


MESSAGE_SETTING = {
    (status.HTTP_404_NOT_FOUND): {
        "model": Message
    },
    status.HTTP_412_PRECONDITION_FAILED : {
        "model": Message
    }
}
# @app.get("/items/{item_id}", response_model=Item, responses={404: {"model": Message}})
# async def read_item(item_id: str):
#     if item_id == "foo":
#         return {"id": "foo", "value": "there goes my hero"}
#     return JSONResponse(status_code=404, content={"message": "Item not found"})
