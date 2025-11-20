import os
from datetime import datetime
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import db, create_document, get_documents
from schemas import Event, Sermon, LifeGroup, PrayerRequest, GalleryItem

app = FastAPI(title="Church Website API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Church API running"}

# Utility

def collection_name(model_cls) -> str:
    return model_cls.__name__.lower()

# Events
@app.get("/api/events")
def list_events(limit: Optional[int] = 50):
    try:
        items = get_documents(collection_name(Event), {}, limit)
        # Convert ObjectId and datetime to serializable
        for it in items:
            it["_id"] = str(it.get("_id"))
            for k, v in list(it.items()):
                if isinstance(v, datetime):
                    it[k] = v.isoformat()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/events", status_code=201)
def create_event(event: Event):
    try:
        inserted_id = create_document(collection_name(Event), event)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Sermons
@app.get("/api/sermons")
def list_sermons(limit: Optional[int] = 100, series: Optional[str] = None, speaker: Optional[str] = None):
    try:
        filt = {}
        if series:
            filt["series"] = series
        if speaker:
            filt["speaker"] = speaker
        items = get_documents(collection_name(Sermon), filt, limit)
        for it in items:
            it["_id"] = str(it.get("_id"))
            for k, v in list(it.items()):
                if isinstance(v, datetime):
                    it[k] = v.isoformat()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/sermons", status_code=201)
def create_sermon(sermon: Sermon):
    try:
        inserted_id = create_document(collection_name(Sermon), sermon)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Life Groups
@app.get("/api/life-groups")
def list_life_groups(limit: Optional[int] = 100):
    try:
        items = get_documents(collection_name(LifeGroup), {}, limit)
        for it in items:
            it["_id"] = str(it.get("_id"))
            for k, v in list(it.items()):
                if isinstance(v, datetime):
                    it[k] = v.isoformat()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/life-groups", status_code=201)
def create_life_group(group: LifeGroup):
    try:
        inserted_id = create_document(collection_name(LifeGroup), group)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Gallery
@app.get("/api/gallery")
def list_gallery(limit: Optional[int] = 100, album: Optional[str] = None):
    try:
        filt = {"album": album} if album else {}
        items = get_documents(collection_name(GalleryItem), filt, limit)
        for it in items:
            it["_id"] = str(it.get("_id"))
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/gallery", status_code=201)
def create_gallery_item(item: GalleryItem):
    try:
        inserted_id = create_document(collection_name(GalleryItem), item)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Prayer Requests
@app.get("/api/prayers")
def list_prayers(limit: Optional[int] = 100, public_only: bool = True):
    try:
        filt = {"is_public": True} if public_only else {}
        items = get_documents(collection_name(PrayerRequest), filt, limit)
        for it in items:
            it["_id"] = str(it.get("_id"))
            for k, v in list(it.items()):
                if isinstance(v, datetime):
                    it[k] = v.isoformat()
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/prayers", status_code=201)
def create_prayer(req: PrayerRequest):
    try:
        inserted_id = create_document(collection_name(PrayerRequest), req)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Contact form model and endpoint
class ContactMessage(BaseModel):
    name: str
    email: str
    message: str

@app.post("/api/contact", status_code=202)
def contact(msg: ContactMessage):
    try:
        # store as a document so it's persisted
        _ = create_document("contactmessage", msg)
        return {"status": "received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
