#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
공인중개사 기출문제 PDF 파싱 스크립트
2025년 제36회 문제를 추출하여 JSON 형식으로 변환
"""

import PyPDF2
import re
import json

def extract_text_from_pdf(pdf_path):
    """PDF에서 텍스트 추출"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    except Exception as e:
        print(f"PDF 읽기 오류: {e}")
    return text

def parse_answers(answer_pdf_path):
    """정답 PDF에서 정답 추출"""
    text = extract_text_from_pdf(answer_pdf_path)
    
    answers = {}
    
    # 1차 1교시 부동산학개론 (1-40)
    pattern_1_1 = r'(\d+)\s+(\d)'
    matches = re.findall(pattern_1_1, text)
    
    for match in matches:
        q_num, answer = match
        answers[int(q_num)] = int(answer) - 1  # 0-based index
    
    return answers

def parse_questions_1st_1st(pdf_path, answers):
    """1차 1교시 문제 파싱 (부동산학개론)"""
    text = extract_text_from_pdf(pdf_path)
    questions = []
    
    # 문제 번호로 분리
    # 패턴: 숫자. 문제내용
    pattern = r'(\d+)\.\s+(.+?)(?=\d+\.|$)'
    
    # 수동으로 파싱 (PDF 구조상 자동화 어려움)
    # 일단 기본 구조만 생성
    
    return questions

def parse_questions_2nd_1st(pdf_path, answers):
    """2차 1교시 문제 파싱 (공인중개사법, 부동산공법)"""
    questions = []
    return questions

def parse_questions_2nd_2nd(pdf_path, answers):
    """2차 2교시 문제 파싱 (부동산공시법 및 세법)"""
    questions = []
    return questions

def generate_javascript_array(all_questions):
    """JavaScript 배열 형식으로 변환"""
    js_code = "const questionDatabase = [\n"
    
    for q in all_questions:
        js_code += "    {\n"
        js_code += f"        year: {q['year']},\n"
        js_code += f"        subject: '{q['subject']}',\n"
        js_code += f"        question: \"{q['question']}\",\n"
        js_code += "        options: [\n"
        for opt in q['options']:
            js_code += f"            \"{opt}\",\n"
        js_code += "        ],\n"
        js_code += f"        correct: {q['correct']},\n"
        js_code += f"        explanation: \"{q['explanation']}\"\n"
        js_code += "    },\n"
    
    js_code += "];\n"
    return js_code

def main():
    """메인 실행 함수"""
    print("🚀 공인중개사 기출문제 파싱 시작...")
    
    # 파일 경로
    pdf_1_1 = "/mnt/user-data/uploads/2025년_제36회_공인중개사_1차_1교시_문제지.pdf"
    pdf_2_1 = "/mnt/user-data/uploads/2025년_제36회_공인중개사_2차_1교시_문제지.pdf"
    pdf_2_2 = "/mnt/user-data/uploads/2025년_제36회_공인중개사_2차_2교시_문제지.pdf"
    pdf_answer = "/mnt/user-data/uploads/2025년_제36회_공인중개사_최종정답.pdf"
    
    # 정답 추출
    print("📊 정답 추출 중...")
    answers = parse_answers(pdf_answer)
    print(f"정답 개수: {len(answers)}")
    
    # 문제 추출
    all_questions = []
    
    print("📖 1차 1교시 문제 추출 중...")
    questions_1_1 = parse_questions_1st_1st(pdf_1_1, answers)
    all_questions.extend(questions_1_1)
    
    print("📖 2차 1교시 문제 추출 중...")
    questions_2_1 = parse_questions_2nd_1st(pdf_2_1, answers)
    all_questions.extend(questions_2_1)
    
    print("📖 2차 2교시 문제 추출 중...")
    questions_2_2 = parse_questions_2nd_2nd(pdf_2_2, answers)
    all_questions.extend(questions_2_2)
    
    # JavaScript 코드 생성
    print("✨ JavaScript 코드 생성 중...")
    js_code = generate_javascript_array(all_questions)
    
    # 파일 저장
    output_path = "/mnt/user-data/outputs/questions_2025.js"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(js_code)
    
    print(f"✅ 완료! 총 {len(all_questions)}개 문제 추출")
    print(f"📁 저장 위치: {output_path}")

if __name__ == "__main__":
    main()