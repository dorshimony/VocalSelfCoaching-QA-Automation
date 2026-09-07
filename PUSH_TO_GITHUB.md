# העלאה לגיטהאב

המאגר כבר קיים וריק:

**https://github.com/dorshimony/VocalSelfCoaching-QA-Automation**

נשאר רק לדחוף אליו את הקבצים. שתי דרכים, בחר אחת.

---

## דרך א — טרמינל של פייצ'ארם

פתח את הפרויקט בפייצ'ארם, ובטרמינל שלו הדבק את השורות האלה אחת אחרי השנייה:

```
git init
git add .
git commit -m "QA automation project for VocalSelfCoaching"
git branch -M main
git remote add origin https://github.com/dorshimony/VocalSelfCoaching-QA-Automation.git
git push -u origin main
```

בדחיפה הראשונה ייתכן שתיפתח חלונית התחברות לגיטהאב. זו התחברות רגילה, פעם אחת.

---

## דרך ב — בלי פקודות

בתפריט העליון של פייצ'ארם:

**Git ← GitHub ← Share Project on GitHub**

בחלונית שנפתחת, בשדה השם הדבק:

```
VocalSelfCoaching-QA-Automation
```

חשוב: אם פייצ'ארם מודיע שהשם כבר תפוס, זה בגלל שהמאגר כבר נוצר. במקרה כזה
עדיף לחזור לדרך א, או למחוק את המאגר הריק בגיטהאב ולתת לפייצ'ארם ליצור אותו מחדש.

---

## אחרי הדחיפה

1. רענן את דף המאגר בדפדפן. אמורים להופיע כל הקבצים, וקובץ ה־README אמור להיות מוצג מתחתם.
2. הקישור לשיתוף הוא כתובת המאגר עצמה.

---

## מה עולה למאגר

```
pages/          שישה קבצי Page Object
tests/          תשעה קבצי בדיקה, 19 בדיקות
evidence/       שלוש הקלטות מסך ושישה צילומי מסך
conftest.py     הגדרות משותפות
pytest.ini      הגדרות הרצה
requirements.txt
README.md
PRODUCT_SPEC.md אפיון המוצר
BUGS.md         דוח באגים בקצרה
BUG_REPORT.html דוח באגים מפורט
BUG_REPORT_WITH_VIDEO.html
.gitignore
```

תיקיות זמניות של פייתון לא יעלו, בזכות קובץ ה־gitignore.
