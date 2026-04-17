from dotenv import load_dotenv
load_dotenv()
try:
    from backend.app.ai_service import analyze_task
    result = analyze_task('Complete assignment', 'Finish PySpark due tomorrow')
    print('SUCCESS:', result)
except Exception as e:
    print('ERROR:', str(e))
