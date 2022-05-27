import uvicorn
from fastapi import FastAPI, File, UploadFile, HTTPException

import numpy as np
from PIL import Image

from helper_utils import get_encoding

app = FastAPI()


@app.post("/image")
def create_upload_file(image: UploadFile = File(...)):
    image = np.array(Image.open(image.file))
    encoding = get_encoding(image)
    if encoding:
        return {"encoding": encoding}
    raise HTTPException(status_code=400, detail="Failed to process image")


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8002, log_level="info")
