# 🛍️ Thai Shopping Review Sentiment Classification  
### Mini Project: Bag-of-Words / TF-IDF + Machine Learning + Streamlit Deployment

<img width="1193" height="817" alt="image" src="https://github.com/user-attachments/assets/c96788b5-fcde-4195-a4b5-3493c330a5d4" />


โปรเจกต์นี้เป็นระบบ **จำแนกความคิดเห็นรีวิวสินค้าออนไลน์ภาษาไทย** ว่าเป็น  
- **Positive (เชิงบวก)**  
- **Negative (เชิงลบ)**  

โดยใช้แนวทาง **Traditional Machine Learning for Text Classification**  
ร่วมกับ **TF-IDF feature extraction** และ deploy เป็น **Streamlit Web App** สำหรับทดลองพิมพ์ข้อความรีวิวและทำนายผลได้แบบ real-time

---

# 📌 Project Overview

ในปัจจุบันรีวิวจากผู้ใช้งานมีความสำคัญต่อการวิเคราะห์คุณภาพสินค้าและประสบการณ์ของลูกค้าอย่างมาก  
โปรเจกต์นี้จึงถูกสร้างขึ้นเพื่อสาธิตการพัฒนา **Thai Text Sentiment Classification** แบบง่าย ๆ ภายในเวลาจำกัด โดยใช้ workflow ที่ชัดเจน ไม่ซับซ้อน และเหมาะสำหรับการเรียนรู้หรือส่งเป็น mini project

### แนวคิดหลักของโปรเจกต์
- ใช้ข้อมูลจากไฟล์ `review_shopping.csv`
- ทำความสะอาดข้อความภาษาไทย
- ตัดคำภาษาไทยด้วย `attacut`
- แปลงข้อความเป็นตัวเลขด้วย **TF-IDF**
- สร้างและเปรียบเทียบอย่างน้อย **2 โมเดล**
- เลือกโมเดลที่ดีที่สุดสำหรับ deploy
- สร้างหน้าเว็บด้วย **Streamlit**

---

# 🎯 Project Objective

## วัตถุประสงค์ของโปรเจกต์
1. เพื่อสร้างโมเดลสำหรับจำแนกข้อความรีวิวสินค้าออนไลน์ภาษาไทย
2. เพื่อเปรียบเทียบประสิทธิภาพของโมเดล Machine Learning อย่างน้อย 2 โมเดล
3. เพื่อเลือกโมเดลที่ดีที่สุดและ export ไปใช้งานจริง
4. เพื่อสร้าง Web Application แบบง่ายด้วย Streamlit สำหรับการทดสอบข้อความใหม่

---

# 🧠 Problem Statement

ข้อความรีวิวสินค้าในโลกจริงมักมีลักษณะดังนี้

- เป็นข้อความภาษาไทย
- มีคำซ้ำเพื่อเน้นอารมณ์ เช่น `ดีมากกกก`, `แย่มากกก`
- มี emoji หรือสัญลักษณ์พิเศษ
- มีภาษาพูดหรือคำสะกดไม่เป็นทางการ
- ไม่มีโครงสร้างตายตัว

ดังนั้น การนำข้อความรีวิวไปสร้างโมเดลจำแนก sentiment จำเป็นต้องมีขั้นตอน preprocessing และ tokenization ที่เหมาะสมกับภาษาไทย

---

# 🗂️ Dataset

ไฟล์ข้อมูลที่ใช้คือ:

```bash
review_shopping.csv
