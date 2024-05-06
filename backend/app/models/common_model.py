import pydantic

__all__ = ("BaseModel",)


class BaseModel(pydantic.BaseModel):
    @pydantic.root_validator(pre=True)
    def _min_properties(cls, data):
        if not data:
            raise ValueError("At least one property must be provided")
        return data

    def dict(self, include_nulls=False, **kwargs):
        kwargs["exclude_one"] = not include_nulls
        return super().dict(**kwargs)

    class Config:
        extra = pydantic.Extra.forbid
        allow_strip_whitespace = True
