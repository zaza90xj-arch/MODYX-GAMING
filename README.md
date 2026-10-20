# MODYX GAMING

هذا المشروع هو بوت Telegram عربي متكامل مع لوحة إدارة ويب FastAPI ومخزن SQLite.

## متطلبات التشغيل
- Python 3.10+
- Termux على Android أو Linux
- اتصال إنترنت للتحميل

## التثبيت السريع
1. افتح Termux
2. نفذ:

```bash
pkg update && pkg upgrade
pkg install python git clang
python -m pip install --upgrade pip
pip install -r requirements.txt
```

3. افتح ملف الإعدادات:

```bash
nano app/config.py
```

4. أضف:
- BOT_TOKEN
- OWNER_TELEGRAM_ID
- REGISTRATION_GROUP_ID (اختياري)
- WEB_ADMIN_USERNAME
- WEB_ADMIN_PASSWORD

5. شغّل البوت:

```bash
python bot.py
```

6. أو شغّل لوحة الويب:

```bash
python web.py
```

7. أو شغّل كلاهما:

```bash
python run.py --service both
```

## ملاحظات مهمة
- لا يوجد ملف `.env` في هذا المشروع.
- جميع الإعدادات الحساسة موجودة في `app/config.py` فقط.
- إذا كانت BOT_TOKEN فارغة، سيظهر تنبيه ويوقف التشغيل بشكل منظم.
- يجب ضبط حسابات لوحة الإدارة يدويًا في `app/config.py`.

## هيكل المشروع
- app/
- app/bot/
- app/database/
- app/services/
- app/web/
- tests/

## اختبارات
```bash
pytest -q
```
