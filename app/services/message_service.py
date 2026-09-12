from app.models import Batch, CurriculumSession, ScheduledSession

class MessageService:
    @staticmethod
    def generate_reminder_message(batch: Batch, curriculum: CurriculumSession, scheduled: ScheduledSession) -> str:
        """
        Generate the HTML message for Telegram based on Batch, Week, Day, and Topic.
        """
        
        # Format the time (assuming 7:00 PM - 8:30 PM format based on 19:00 default)
        start_time_str = curriculum.default_start_time.strftime("%I:%M %p").lstrip('0')
        
        # Calculate end time strictly for display
        # We know duration is 90 mins, so 8:30 PM
        # This is a basic approach; in reality, we could do timedelta math if needed.
        end_time_str = "8:30 PM" if curriculum.default_duration_minutes == 90 else "TBD"

        # Format topics into bullet points (assuming topics are comma-separated in the DB)
        topic_lines = [t.strip() for t in curriculum.topic.split(',') if t.strip()]
        topics_bulleted = "\n".join([f"🤖 {t}" for t in topic_lines])

        message = (
            f"📢 <b>{batch.name} — Week #{curriculum.week_number} — {curriculum.category}</b> 🎬🤖\n"
            f"అందరికీ నమస్కారం! 👋\n\n"
            f"ఈ రోజు మన session లో\n"
            f"✨ <b>{curriculum.category}</b>\n"
            f"పై practical గా discuss చేద్దాం.\n\n"
            f"ఈ session లో మనం:\n"
            f"{topics_bulleted}\n\n"
            f"అలాగే మన course లో upcoming sessions ఎలా ఉండబోతున్నాయి, ఏ tools నేర్చుకోబోతున్నాం, వాటిని practical projects లో ఎలా use చేయబోతున్నాం అనే విషయాలను కూడా తెలుసుకుందాం. 🔥\n\n"
            f"⏰ <b>Today at {start_time_str}</b>\n"
            f"💻 Please be ready with your laptop & stable internet.\n\n"
            f"🔗 <b>Zoom Link:</b>\n{scheduled.zoom_join_url}\n\n"
            f"See you all in the session! 😊🔥\n\n"
            f"~ AI Film Makers"
        )
        return message
        
    @staticmethod
    def generate_zoom_topic(batch: Batch, curriculum: CurriculumSession) -> str:
        """Generate Zoom Meeting Topic"""
        return f"{batch.name} — Week #{curriculum.week_number} — {curriculum.category}"
