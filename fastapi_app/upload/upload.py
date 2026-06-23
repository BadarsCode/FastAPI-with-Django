from pathlib import Path
from typing import Annotated, List, Optional

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse

router = APIRouter()
UPLOAD_DIR = Path(__file__).resolve().parents[1] / "file"


async def save_uploaded_file(file: UploadFile) -> dict:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = Path(file.filename or "uploaded_file").name
    content = await file.read()
    file_path = UPLOAD_DIR / filename

    with file_path.open("wb") as buffer:
        buffer.write(content)

    return {
        "filename": filename,
        "size": len(content),
        "path": str(file_path),
    }


@router.post('/upload')
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    return {
        'filename': file.filename,
        'size': len(content),
    }


@router.post('/save-file')
async def save_file(file: UploadFile = File(...)):
    saved_file = await save_uploaded_file(file)
    return {
        'message': 'File Saved Successfully',
        'file': saved_file,
    }


@router.post("/upload-multiple")
async def upload_files(
    files: Optional[List[UploadFile]] = File(default=None),
    file: Optional[List[UploadFile]] = File(default=None),
    files_brackets: Optional[List[UploadFile]] = File(default=None, alias="files[]"),
):
    uploaded_files = files or file or files_brackets

    if not uploaded_files:
        raise HTTPException(
            status_code=422,
            detail="Upload one or more files using the form field 'files'.",
        )

    saved_files = []

    for uploaded_file in uploaded_files:
        saved_files.append(await save_uploaded_file(uploaded_file))

    return {
        "message": "Files Saved Successfully",
        "files": saved_files,
    }


@router.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    return {"filename": file.filename}


@router.post("/files/")
async def create_files(files: Annotated[list[UploadFile], File()]):
    file_sizes = []

    for file in files:
        content = await file.read()
        file_sizes.append(len(content))

    return {"file_sizes": file_sizes}


@router.post("/uploadfiles/")
async def create_upload_files(files: Annotated[list[UploadFile], File()]):
    return {"filenames": [file.filename for file in files]}


@router.get("/multiplefiles/")
async def main():
    content = """
<body>
<form action="/upload-multiple" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
