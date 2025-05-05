
# Image OCR Renamer

这个项目的背景是需要将很多个微信群的二维码图片重命名成其对应的课程，并转换格式，方便给后端机器人使用。

This tool converts a batch of `.jpg` images (e.g., WeChat QR code posters) into `.png` format, extracts course codes via OCR, and renames each image accordingly.

---

## 🔧 Features

- 🔁 Batch convert JPG → PNG
- 🧠 Smart OCR-based course code detection (e.g., `CS6310`, `MGT8813`, `CS8803O15`)
- 📐 Auto-crop upper region for fallback OCR if full-image fails
- 💡 Preprocess with grayscale + binarization for better OCR accuracy
- 📊 Logs success & failure count with `unknown_XX.png` fallback names

---

## 🗂️ Folder Structure

```
project/
│
├── input_images/              # Put your JPG files here
├── converted_png/             # Output folder (auto-created)
├── main.py                    # Script file
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

1. **Clone the project**
2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR:**

   - macOS: `brew install tesseract`
   - Ubuntu: `sudo apt install tesseract-ocr`
   - Windows: [Download here](https://github.com/tesseract-ocr/tesseract)

4. **Run the script**

   ```bash
   python main.py
   ```

---

## ✅ Example Result

| Input File              | OCR Result        | Output File     |
|-------------------------|-------------------|------------------|
| A jpg file which contains `CS6310` | `CS6310`          | `CS6310.png`     |
| A jpg file which contains `CS8803O15` | `CS8803O15`       | `CS8803O15.png`  |
| An unreadable jpg file | _OCR failed_      | `unknown_01.png` |

---

## 📌 Notes

- OCR is language-agnostic by default (`lang='eng'`).
- If needed, you can install more Tesseract languages via `brew install tesseract-lang` (macOS).

---

## 📄 License

MIT License
