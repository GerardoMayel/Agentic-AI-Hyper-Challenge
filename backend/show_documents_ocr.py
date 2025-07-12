#!/usr/bin/env python3
from sqlalchemy import create_engine, text
from app.core.database import DATABASE_URL

engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM documents_ocr ORDER BY id DESC LIMIT 10"))
    for row in result:
        print("-" * 60)
        for k, v in dict(row).items():
            print(f"{k}: {v}") 