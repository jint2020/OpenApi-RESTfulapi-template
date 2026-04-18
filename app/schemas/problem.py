from pydantic import BaseModel, Field


class InvalidParam(BaseModel):
    name: str = Field(..., description="出错的参数/字段名")
    reason: str = Field(..., description="错误原因")


class ProblemDetails(BaseModel):
    type: str = Field(..., description="错误类型 URI")
    title: str = Field(..., description="错误标题")
    status: int = Field(..., description="HTTP 状态码")
    detail: str = Field(..., description="错误详情")
    instance: str = Field(..., description="发生错误的请求路径")
    invalid_params: list[InvalidParam] | None = Field(default=None, description="参数错误详情")
