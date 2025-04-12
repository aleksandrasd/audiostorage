from pydantic import BaseModel, Field


class Pagination(BaseModel):
    total_records: int = Field(
        ...,
        title="Total Records",
        description="The total number of records available."
    )
    current_page: int = Field(
        ...,
        title="Current Page",
        description="The current page number."
    )
    total_pages: int = Field(
        ...,
        title="Total Pages",
        description="The total number of pages available."
    )
    next_page: int | None = Field(
        ...,
        title="Next Page",
        description="The next page number. Null if there is no next page."
    )
    prev_page: int | None = Field(
        None,
        title="Previous Page",
        description="The previous page number. Null if there is no previous page."
    )
    @classmethod
    def create(cls, data: any, offset: int, limit: int, total_records: int):
        total_pages = (total_records + limit - 1) // limit  
        current_page = (offset // limit) + 1 if total_records > 0 else 1
        
        next_page = current_page + 1 if current_page < total_pages else None
        prev_page = current_page - 1 if current_page > 1 else None

        return cls(
            data=data,
            total_records=total_records,
            current_page=current_page,
            total_pages=total_pages,
            next_page=next_page,
            prev_page=prev_page,
        )
  