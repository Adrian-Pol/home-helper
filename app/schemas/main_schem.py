
from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel, Field


class RequestModel(BaseModel):
    @classmethod
    async def from_request(cls, request: Request):
        content_type = request.headers.get("content-type", "").lower()

        
        data = dict(request.query_params)

        
        if content_type.startswith("application/json"):
            body = await request.json()
            if isinstance(body, dict):
                data.update(body)

        elif (
            content_type.startswith("application/x-www-form-urlencoded")
            or content_type.startswith("multipart/form-data")
        ):
            form = await request.form()
            data.update(form)

        
        if not data:
            raise ValueError("No data provided")

        return cls(**data)



