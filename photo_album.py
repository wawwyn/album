import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

class PhotoAlbum:
    def __init__(self, root):
        self.root = root
        self.root.title("사진 앨범")
        self.root.geometry("800x600")
        
        # 현재 이미지 경로와 이미지 리스트
        self.current_image_path = None
        self.image_list = []
        self.current_index = 0
        
        self.create_widgets()
        
    def create_widgets(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 이미지 표시 영역
        self.image_label = ttk.Label(main_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # 버튼들
        ttk.Button(button_frame, text="이미지 추가", command=self.add_images).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="이전", command=self.prev_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="다음", command=self.next_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="삭제", command=self.delete_image).pack(side=tk.LEFT, padx=5)
        
        # 상태 표시줄
        self.status_var = tk.StringVar()
        self.status_var.set("이미지를 추가해주세요")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.pack(pady=5)
        
    def add_images(self):
        file_paths = filedialog.askopenfilenames(
            title="이미지 선택",
            filetypes=[
                ("이미지 파일", "*.jpg *.jpeg *.png *.gif *.bmp"),
                ("모든 파일", "*.*")
            ]
        )
        
        if file_paths:
            self.image_list.extend(file_paths)
            if not self.current_image_path:
                self.current_index = 0
                self.show_image(self.image_list[0])
            self.update_status()
            
    def show_image(self, image_path):
        try:
            # 이미지 로드 및 크기 조정
            image = Image.open(image_path)
            
            # 이미지 크기 조정 (최대 600x400)
            display_size = (600, 400)
            image.thumbnail(display_size, Image.Resampling.LANCZOS)
            
            # PhotoImage로 변환
            photo = ImageTk.PhotoImage(image)
            
            # 이미지 표시
            self.image_label.configure(image=photo)
            self.image_label.image = photo  # 참조 유지
            
            self.current_image_path = image_path
            self.update_status()
            
        except Exception as e:
            messagebox.showerror("오류", f"이미지를 불러올 수 없습니다: {str(e)}")
            
    def prev_image(self):
        if self.image_list and self.current_index > 0:
            self.current_index -= 1
            self.show_image(self.image_list[self.current_index])
            
    def next_image(self):
        if self.image_list and self.current_index < len(self.image_list) - 1:
            self.current_index += 1
            self.show_image(self.image_list[self.current_index])
            
    def delete_image(self):
        if not self.current_image_path:
            return
            
        if messagebox.askyesno("확인", "현재 이미지를 삭제하시겠습니까?"):
            try:
                # 파일 시스템에서 삭제
                os.remove(self.current_image_path)
                # 리스트에서 제거
                self.image_list.remove(self.current_image_path)
                
                # 다음 이미지 표시
                if self.image_list:
                    if self.current_index >= len(self.image_list):
                        self.current_index = len(self.image_list) - 1
                    self.show_image(self.image_list[self.current_index])
                else:
                    self.current_image_path = None
                    self.image_label.configure(image='')
                    self.update_status()
                    
            except Exception as e:
                messagebox.showerror("오류", f"이미지를 삭제할 수 없습니다: {str(e)}")
                
    def update_status(self):
        if self.image_list:
            self.status_var.set(f"이미지 {self.current_index + 1}/{len(self.image_list)}: {os.path.basename(self.current_image_path)}")
        else:
            self.status_var.set("이미지를 추가해주세요")

if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoAlbum(root)
    root.mainloop() 