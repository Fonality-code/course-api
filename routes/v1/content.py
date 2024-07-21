from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, Response, status
from typing import List

from bson.errors import InvalidId

from models.errors import ErrorResponse


router = APIRouter(
    prefix='/content',
    tags=['content']
)


from models.courses import Course


from models.content import(
    Content,
    CreateContent,
    UpdateContent
    
)


@router.get('/', response_model=List[Content])
async def get_contents():
    try:
        content = await Content.find_all().to_list()
        return content
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    


@router.get('/{id}', response_model=Content)
async def get_content(id: str):
    try: 

        id = PydanticObjectId(id)
        content = await Content.get(id)
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        return content
    except InvalidId:
        raise HTTPException(status_code=404, detail="Invalid ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/', response_model=Content)
async def create_content(content: CreateContent):

    # check if course with the id exist 
    course = await Course.get(content.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    try:
        content_doc = Content(**content.model_dump())
        await content_doc.insert()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return content


@router.get('/course/{id}')
async def get_contents_by_course(id: str):
    try:
        PydanticObjectId(id)
        contents = await Content.find({'course_id': id}).to_list()
        return contents
    except InvalidId:
        raise HTTPException(status_code=404, detail="Invalid ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.put('/{id}')
async def update_content(id: str, content: UpdateContent):
    try:
        id = PydanticObjectId(id)
        content_doc = await Content.get(id)
        if not content_doc:
            raise HTTPException(status_code=404, detail="Content not found")
        update_data = content.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(content_doc, key, value)
        await content_doc.save()
        return content_doc
    except InvalidId:
        raise HTTPException(status_code=404, detail="Invalid ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.delete('/{id}')
async def delete_content(id: str):
    try:
        id = PydanticObjectId(id)
        content = await Content.get(id)
        if not content:
            raise HTTPException(status_code=404, detail="Content not found")
        await content.delete()
        return {
            "message": "Content deleted successfully"
        
        }
    except InvalidId:
        raise HTTPException(status_code=404, detail="Invalid ID")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))