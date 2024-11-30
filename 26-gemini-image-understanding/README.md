## Gemini Image  Understanding


1. เปลี่ยนไปยังโฟลเดอร์โปรเจกต์
ใช้คำสั่ง cd เพื่อเปลี่ยนไปยังโฟลเดอร์ชื่อ 26-gemini-image-understanding/
```
cd 26-gemini-image-understanding/
```

2. คัดลอกไฟล์ตัวอย่างการตั้งค่า
คำสั่ง cp ใช้เพื่อคัดลอกไฟล์ vertex_ai_secret.yml.example และเปลี่ยนชื่อเป็น vertex_ai_secret.yml เพื่อใช้เป็นไฟล์ตั้งค่าหลัก

```
cp vertex_ai_secret.yml.example vertex_ai_secret.yml
```

3. ติดตั้ง Dependencies ของโปรเจกต์
ใช้คำสั่ง pip เพื่อติดตั้งไลบรารีทั้งหมดที่ระบุไว้ในไฟล์ requirements.txt

```
pip install -r requirements.txt
```

4. Call python ให้ Gemini ช่วอธิบายรูปภาพ
ใช้คำสั่ง python เพื่อรันไฟล์ gemini_image_understanding.py ซึ่งเป็นสคริปต์หลักของโปรเจกต์

```
python gemini_image_understanding.py
```
