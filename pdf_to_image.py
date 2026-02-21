import fitz
import pytesseract
import cv2
import numpy as np
import os
import re
from PIL import Image
from tkinter import Tk, filedialog, messagebox, ttk
import threading
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# ===== 설정 =====
DPI = 300
QUESTION_PATTERN = re.compile(r'^\d+\.')

# ===== 2단 자동 인식 =====
def detect_columns(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    vertical_sum = np.sum(gray, axis=0)

    threshold = np.mean(vertical_sum) * 0.98
    gap_indices = np.where(vertical_sum > threshold)[0]

    if len(gap_indices) < 50:
        w = image.shape[1]
        return [(0, w//2), (w//2, w)]

    mid = np.median(gap_indices)
    return [(0, int(mid)), (int(mid), image.shape[1])]

# ===== OCR로 문제 번호 위치 찾기 =====
def find_question_positions(image):
    data = pytesseract.image_to_data(
        image,
        lang='kor+eng',
        output_type=pytesseract.Output.DICT
    )

    positions = []

    for i, text in enumerate(data['text']):
        text = text.strip()

        if not text:
            continue

        number_match = re.match(r'^(\d+)', text)
        if number_match:
            try:
                q_num = int(number_match.group(1))
                y = data['top'][i]
                positions.append((q_num, y))
            except:
                continue

    positions.sort(key=lambda x: x[1])
    return positions

# ===== 문제별 이미지 추출 =====
def extract_questions(pdf_path, progress_callback=None):

    doc = fitz.open(pdf_path)
    output_dir = os.path.join(os.path.dirname(pdf_path), "FINAL_EXTRACTED")
    os.makedirs(output_dir, exist_ok=True)

    total_pages = len(doc)

    for page_num in range(total_pages):

        page = doc[page_num]
        mat = fitz.Matrix(DPI/72, DPI/72)
        pix = page.get_pixmap(matrix=mat)
        img = np.frombuffer(pix.samples, dtype=np.uint8)
        img = img.reshape(pix.height, pix.width, pix.n)

        if pix.n == 4:
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

        columns = detect_columns(img)

        for col_index, (x_start, x_end) in enumerate(columns):

            col_img = img[:, x_start:x_end]

            questions = find_question_positions(col_img)

            for i, (q_num, y_start) in enumerate(questions):

                if i + 1 < len(questions):
                    y_end = questions[i+1][1]
                else:
                    y_end = col_img.shape[0] - 10

                if y_end - y_start < 50:
                    continue

                question_img = col_img[y_start:y_end, :]

                filename = f"P{page_num+1}_Q{str(q_num).zfill(2)}.png"
                save_path = os.path.join(output_dir, filename)

                cv2.imwrite(save_path, question_img)

        if progress_callback:
            progress_callback((page_num + 1) / total_pages * 100)

    doc.close()

# ===== GUI =====
class App:

    def __init__(self, root):
        self.root = root
        self.root.title("시험지 문제 자동 추출기 v10 Ultimate")
        self.root.geometry("500x200")

        self.label = ttk.Label(root, text="PDF 파일을 선택하세요")
        self.label.pack(pady=10)

        self.button = ttk.Button(root, text="파일 선택", command=self.select_file)
        self.button.pack(pady=5)

        self.progress = ttk.Progressbar(root, length=400)
        self.progress.pack(pady=20)

    def select_file(self):
        # 🔥 반드시 메인 스레드에서 실행
        file_path = filedialog.askopenfilename(
            title="PDF 파일 선택",
            filetypes=[("PDF files", "*.pdf")]
        )

        if not file_path:
            return

        # 🔥 무거운 작업만 스레드로
        threading.Thread(
            target=self.run_extraction,
            args=(file_path,),
            daemon=True
        ).start()

    def update_progress(self, value):
        self.progress["value"] = value
        self.root.update_idletasks()

    def run_extraction(self, file_path):
        try:
            extract_questions(file_path, self.update_progress)
            messagebox.showinfo("완료", "문제 추출 완료!\n폴더: FINAL_EXTRACTED")
        except Exception as e:
            messagebox.showerror("오류", str(e))

if __name__ == "__main__":
    root = Tk()
    root.withdraw()  # 메인창 숨김

    file_path = filedialog.askopenfilename(
        title="PDF 파일 선택",
        filetypes=[("PDF files", "*.pdf")]
    )

    if file_path:
        extract_questions(file_path)
        messagebox.showinfo("완료", "문제 추출 완료!\n폴더: FINAL_EXTRACTED")

    root.destroy()