"""
Database Schemas for Church Website

Each Pydantic model maps to a MongoDB collection with the lowercase name
(e.g., Event -> "event").
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
from datetime import datetime

class Event(BaseModel):
    title: str = Field(..., description="Event title")
    description: str = Field(..., description="Short description of the event")
    date: datetime = Field(..., description="Event date and time")
    image_url: Optional[HttpUrl] = Field(None, description="Image representing the event")
    category: str = Field(..., description="Type of event, e.g., Outreach, Youth, Worship")

class Sermon(BaseModel):
    title: str = Field(..., description="Sermon title")
    speaker: str = Field(..., description="Speaker name")
    series: Optional[str] = Field(None, description="Series name if applicable")
    date: datetime = Field(..., description="Sermon date")
    video_url: Optional[HttpUrl] = Field(None, description="Link to video recording")
    audio_url: Optional[HttpUrl] = Field(None, description="Link to audio recording")
    notes: Optional[str] = Field(None, description="Written notes or link to transcript")

class LifeGroup(BaseModel):
    name: str = Field(..., description="Group name")
    leader: str = Field(..., description="Leader name")
    meeting_day: str = Field(..., description="Day of week the group meets")
    meeting_time: str = Field(..., description="Time the group meets")
    location: str = Field(..., description="Location or area")
    description: Optional[str] = Field(None, description="Short overview of the group focus")
    signup_url: Optional[HttpUrl] = Field(None, description="External sign-up link if any")

class PrayerRequest(BaseModel):
    name: Optional[str] = Field(None, description="Name of the person requesting prayer")
    email: Optional[str] = Field(None, description="Contact email")
    request: str = Field(..., description="Prayer request details")
    is_public: bool = Field(False, description="If true, can be displayed to others")

class GalleryItem(BaseModel):
    title: str = Field(..., description="Caption or title")
    media_type: str = Field(..., description="photo or video")
    url: HttpUrl = Field(..., description="Media URL")
    album: Optional[str] = Field(None, description="Album name: services, missions, events, etc.")

# The Flames database viewer will automatically use these schemas for validation.
