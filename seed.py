import sys
from datetime import time
from app.database import SessionLocal, Base, engine
from app.models import Course, Batch, BatchDay, CurriculumSession

def run_seed():
    db = SessionLocal()
    
    # Check if course exists
    course = db.query(Course).filter(Course.name == "AI Creator Masterclass").first()
    if not course:
        course = Course(name="AI Creator Masterclass")
        db.add(course)
        db.commit()
        db.refresh(course)
        print("Created Course: AI Creator Masterclass")

    # Batches
    batch_data = [
        {"name": "Batch #2", "week": 4, "days": ["MONDAY", "FRIDAY"]},
        {"name": "Batch #3", "week": 1, "days": ["SATURDAY", "SUNDAY"]}
    ]
    
    for b_info in batch_data:
        batch = db.query(Batch).filter(Batch.name == b_info["name"]).first()
        if not batch:
            batch = Batch(course_id=course.id, name=b_info["name"], current_week=b_info["week"])
            db.add(batch)
            db.commit()
            db.refresh(batch)
            print(f"Created Batch: {batch.name}")
            
            for day in b_info["days"]:
                db.add(BatchDay(batch_id=batch.id, day_of_week=day))
            db.commit()

    # Curriculum Data
    # List of (week_number, day_of_week, category, topic)
    curriculum_data = [
        # Week 0 (Assuming Sat/Sun based on Batch 3 structure, modify as needed)
        (0, "SATURDAY", "Orientation", "Master Basics of Prompting with AI Film Maker's Bible"),
        (0, "SUNDAY", "Feedback", "Feedback"),
        
        # Week 1
        (1, "SATURDAY", "AI Youtube Channel", "Create a Brand, Create a YouTube Channel, Upload Your First Video"),
        (1, "SUNDAY", "AI Youtube Channel", "Upload Your First Video"), # Placeholder split, modify explicitly later
        
        # Week 2
        (2, "MONDAY", "Brand Ads", "Product Ad Basics, Product Ad Generation, Isolate Sounds"),
        (2, "FRIDAY", "Feedback Session", "Krishna Photo Tutorial, Character DNA, Location DNA, Cinematic DNA"),
        
        # Week 3
        (3, "MONDAY", "Multi Character AI + Lip Sync", "Multi Character, VFX Basics, PRO Tool Access"),
        (3, "FRIDAY", "Feedback", "Revision, Tools Access, Cartoon Story Videos"),
        
        # Week 4
        (4, "MONDAY", "iPhone Commercials", "Cinematic Commercials"),
        (4, "FRIDAY", "Real Estate Videos", "Luxury Real Estate"),
        
        # Week 5
        (5, "MONDAY", "Mahabharata Videos (Part 1)", "Mahabharata Story Telling Videos"),
        (5, "FRIDAY", "Mahabharata Videos (Part 2)", "Mahabharata Story Lip Sync and Assignments"),
        
        # Week 6
        (6, "MONDAY", "Automobile Ads", "Automobile Ads + VN Editor + Voice Over ElevenLabs"),
        (6, "FRIDAY", "AI VFX", "AI VFX + Object Replace + Character Replace"),
        
        # Week 7
        (7, "MONDAY", "AI VFX + AI UGC", "Object VFX + AI UGC Introduction + Character Designing"),
        (7, "FRIDAY", "AI UGC & AI CLONE", "AI UGC + AI CLONE + AI MUSIC"),
        
        # Week 8
        (8, "MONDAY", "MCP + Portfolio", "MCP + Portfolio"),
        (8, "FRIDAY", "Strategies + Tips", "Strategies + Tips"),
    ]

    for week, day, category, topic in curriculum_data:
        existing = db.query(CurriculumSession).filter(
            CurriculumSession.course_id == course.id,
            CurriculumSession.week_number == week,
            CurriculumSession.day_of_week == day
        ).first()
        
        if not existing:
            session = CurriculumSession(
                course_id=course.id,
                week_number=week,
                day_of_week=day,
                category=category,
                topic=topic,
                default_start_time=time(19, 0) # 19:00 IST
            )
            db.add(session)
    
    db.commit()
    print("Curriculum seeded successfully.")
    db.close()

if __name__ == "__main__":
    print("Starting database seed...")
    run_seed()
    print("Done.")
