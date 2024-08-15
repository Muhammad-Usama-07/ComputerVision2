# import tkinter as tk
# from tkinter import filedialog
# from PIL import Image, ImageTk
# import os
# import json

# class ImageApp:
#     def __init__(self, master):
#         self.master = master
#         self.master.title("Image Pointer")
#         self.canvas = tk.Canvas(self.master)

#         self.image_paths = []
#         self.current_image_index = -1
#         self.image = None
#         self.image_tk = None
#         self.img_width = 0
#         self.img_height = 0
#         self.point_ids = {}
#         # self.point_ids = []
#         self.point_count = 0  # Initialize point count

#         self.create_widgets()

#     def create_widgets(self):
#         self.btn_previous = tk.Button(self.master, text="Previous", command=self.previous_image)
#         self.btn_previous.pack(side=tk.LEFT, padx=5, pady=5)

#         self.btn_next = tk.Button(self.master, text="Next", command=self.next_image)
#         self.btn_next.pack(side=tk.LEFT, padx=5, pady=5)

#         self.btn_undo = tk.Button(self.master, text="Undo", command=self.undo_point)
#         self.btn_undo.pack(side=tk.LEFT, padx=5, pady=5)

#         self.btn_save = tk.Button(self.master, text="Save File", command=self.save_annotation)
#         self.btn_save.pack(side=tk.LEFT, padx=5, pady=5)

#         # self.btn_choose_folder = tk.Button(self.master, text="Choose Folder", command=self.choose_folder)
#         # self.btn_choose_folder.pack(side=tk.LEFT, padx=5, pady=5)
#         self.btn_choose_file = tk.Button(self.master, text="Choose Annotation File", command=self.choose_annotation_file)
#         self.btn_choose_file.pack(side=tk.LEFT, padx=5, pady=5)
#         self.canvas.pack(expand=True, fill=tk.BOTH)
#         self.canvas.bind("<Button-1>", self.draw_point)

#     def load_image(self, file_path):
#         self.image = Image.open(file_path)
#         self.img_width, self.img_height = self.image.size
#         self.image_tk = ImageTk.PhotoImage(self.image)

#         self.canvas.config(width=self.img_width, height=self.img_height)
#         self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)

#     def load_image_from_folder(self, folder_path):
#         # self.image_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith(('png', 'jpg', 'jpeg', 'gif'))]
#         with open(folder_path, 'r') as f:
#             self.annotations = json.load(f)
        
#         self.image_paths = [i['img_path'] for i in self.annotations]
#         # print('----- self.image_paths: ', self.image_paths)
#         self.current_image_index = 0
#         self.load_image(self.image_paths[self.current_image_index])

#     def choose_annotation_file(self):
#         file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
#         print('file_path', file_path)
#         if file_path:
#             self.load_image_from_folder(file_path)

#     def load_annotation(self, file_path):
#         with open(file_path, 'r') as f:
#             self.annotations = json.load(f)
#         # print('----- self.annotations: ', self.annotations[0])
#         self.current_image_index = 0
#         self.load_image()

#     def next_image(self):
#         if self.current_image_index < len(self.image_paths) - 1:
#             self.current_image_index += 1
#             self.point_ids = {}
#             self.point_count =0
#             self.load_image(self.image_paths[self.current_image_index])

#     def previous_image(self):
#         if self.current_image_index > 0:
#             self.current_image_index -= 1
#             self.load_image(self.image_paths[self.current_image_index])
#             self.point_count = 0

#     def draw_point(self, event):
#         if self.image:
#             x, y = event.x, event.y
#             self.point_count +=1

#             point_id = self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="red")
#             print('point_id', point_id)
#             # self.point_ids.append(point_id)
#             label_id = self.canvas.create_text(x + 5, y - 5, text=str(self.point_count), fill="black")
#             self.point_ids[point_id] = [x, y, 1, label_id]
#             # label = tk.Label(self.canvas, text=str(self.point_count), bg="white", bd=1, relief=tk.SOLID)
#             # label.place(x=x+5, y=y)
#             # self.point_ids[point_id] = [x, y, 1]
#             print("Point Position dictionary :", self.point_ids)

#     def undo_point(self):
#         if self.point_ids:
#             # last_point_id = self.point_ids.pop()
#             # print('last_point_id', last_point_id)
#             last_key_to_delete = list(self.point_ids.keys())[-1]
#             if last_key_to_delete in self.point_ids:
#                 self.canvas.delete(int(last_key_to_delete))
#                 self.canvas.delete(self.point_ids[last_key_to_delete][3])
#                 del self.point_ids[last_key_to_delete]
#                 # print(f"The item with key '{last_key_to_delete}' has been deleted.")
#                 # print('new diciotanry is ',self.point_ids )
#                 self.point_count -= 1
#             else:
#                 print(f"The key '{last_key_to_delete}' does not exist in the dictionary.")
#             # print('last_key_to_delete', last_key_to_delete)
#             # self.canvas.delete(int(last_key_to_delete))

#     def save_annotation(self):
#         print('self.image_paths[self.current_image_index]', self.image_paths[self.current_image_index])
#         # for d in  self.annotations:
#         #     if self.image_paths[self.current_image_index] in d['img_path']:
#         #         for k,val in self.point_ids.items():
#         #             d['joints'].append(val)

#         #             print('ddddddddddddddd', d)
#         for i,d in  enumerate(self.annotations):
#             if self.image_paths[self.current_image_index] in d['img_path']:
#                 for k,val in self.point_ids.items():
#                     del val[3]
#                     d['joints'].append(val)
#                     ### i work
#                     self.annotations[i] = d
#                 # print('i',i)
#                 print('ddddddddddddddd', d)
#         print('aaaaaaaaaaaaaaaaaaaaaaaaa', self.annotations)
#         # Save to JSON file
#         with open('check111.json', 'w') as json_file:
#             json.dump(self.annotations, json_file, indent=4)
#             # else:
#             #     print('******** image not exits')    
#         # if self.image_paths[self.current_image_index] in self.annotations[0]['img_path']:
#         #     # print('============== annotations[0][', self.annotations[0])
#         #     # self.annotations[0]['img_path'].append([1,2,3])
#         #     print('annotation before: ',self.annotations[0])
#         #     if len(self.point_ids) > 1:
#                 # for k,val in self.point_ids.items():
#                 #     self.annotations[0]['joints'].append(val)
#         #         print('annotation after: ',self.annotations[0])
#         # else:
#         #     print('******** image not exits')
#         # print('point_ids', self.point_ids)
#         # print('self.image_paths[self.current_image_index]', self.image_paths[self.current_image_index])
#         # file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
#         # print('self.annotations')
#         # if file_path:
#         #     with open(file_path, 'w') as f:
#         #         json.dump(self.annotations, f, indent=4)

# def main():
#     root = tk.Tk()
#     app = ImageApp(root)
#     root.mainloop()

# if __name__ == "__main__":
#     main()



import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os
import json
import cv2
class ImageApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Pointer")
        self.canvas = tk.Canvas(self.master)

        self.image_paths = []
        self.current_image_index = -1
        self.image = None
        self.image_tk = None
        self.img_width = 0
        self.img_height = 0
        self.point_ids = {}
        self.point_count = 0  # Initialize point count

        self.create_widgets()

    def create_widgets(self):
        self.btn_previous = tk.Button(self.master, text="Previous", command=self.previous_image)
        self.btn_previous.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_next = tk.Button(self.master, text="Next", command=self.next_image)
        self.btn_next.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_undo = tk.Button(self.master, text="Undo", command=self.undo_point)
        self.btn_undo.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_save = tk.Button(self.master, text="Save File", command=self.save_annotation)
        self.btn_save.pack(side=tk.LEFT, padx=5, pady=5)

        self.btn_choose_file = tk.Button(self.master, text="Choose Annotation File", command=self.choose_annotation_file)
        self.btn_choose_file.pack(side=tk.LEFT, padx=5, pady=5)
        self.canvas.pack(expand=True, fill=tk.BOTH)
        self.canvas.bind("<Button-1>", self.draw_point)
        
        self.saved_label = tk.Label(self.master, text="", fg="green")
        self.saved_label.pack(side=tk.BOTTOM)
    
    def visualize_image(self, img_path, joints):
        # Read the image
        print('image', img_path)
        img = cv2.imread(img_path)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Draw bounding box
        # x, y, w, h = img_bbox
        # cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)  # Draw rectangle with red color

        # Draw joints
        for idx, joint in enumerate(joints):
            x, y, v = joint
            x, y = int(x), int(y)  # Convert coordinates to integers
            if v == 1:
                cv2.circle(img, (x, y), 5, (0, 0, 255), -1)  # Draw blue circle if joint is visible
            else:
                cv2.circle(img, (x, y), 5, (0, 255, 0), -1)  # Draw green circle if joint is not visible

        # Convert OpenCV image to PIL image
        img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        # Return the image
        return img_pil, img.shape[1], img.shape[0]

    def load_image(self, file_path):

        # self.image = Image.open(file_path)
        # self.img_width, self.img_height = self.image.size
        # self.image_tk = ImageTk.PhotoImage(self.image)

        for i, d in enumerate(self.annotations):
            if file_path in d['img_path']:
                print(d)
                print('exits')
                self.image, img_width, img_height = self.visualize_image(file_path, d['joints'] )  # Call visualize_image function
                self.img_width, self.img_height = self.image.size
                self.image_tk = ImageTk.PhotoImage(self.image)


                self.canvas.config(width=self.img_width, height=self.img_height)
                self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk)
            else:
                pass
                # print('not exits')
        

    def load_image_from_folder(self, folder_path):
        with open(folder_path, 'r') as f:
            self.annotations = json.load(f)
        
        self.image_paths = [i['img_path'] for i in self.annotations]
        self.current_image_index = 0
        self.load_image(self.image_paths[self.current_image_index])

    def choose_annotation_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            self.load_image_from_folder(file_path)

    def next_image(self):
        if self.current_image_index < len(self.image_paths) - 1:
            self.current_image_index += 1
            self.point_ids = {}
            self.point_count = 0  # Reset point count
            self.load_image(self.image_paths[self.current_image_index])
            self.saved_label.config(text="")

    def previous_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image(self.image_paths[self.current_image_index])
            self.point_count = 0  # Reset point count
            self.saved_label.config(text="")

    def draw_point(self, event):
        if self.image:
            x, y = event.x, event.y
            self.point_count += 1

            point_id = self.canvas.create_oval(x-2, y-2, x+8, y+8, fill="blue")
            label_id = self.canvas.create_text(x + 5, y - 5, text=str(self.point_count), fill="black")
            self.point_ids[point_id] = [x, y, 1, label_id]
            print("Point Position dictionary :", self.point_ids)

    def undo_point(self):
        if self.point_ids:
            last_key_to_delete = list(self.point_ids.keys())[-1]
            if last_key_to_delete in self.point_ids:
                self.canvas.delete(int(last_key_to_delete))
                if len(self.point_ids[last_key_to_delete]) > 3:
                    self.canvas.delete(self.point_ids[last_key_to_delete][3])
                del self.point_ids[last_key_to_delete]
                self.point_count -= 1
            self.saved_label.config(text="")

    def save_annotation(self):
        for i, d in enumerate(self.annotations):
            if self.image_paths[self.current_image_index] in d['img_path']:
                for k, val in self.point_ids.items():
                    if len(val) > 3:
                        del val[3]
                    d['joints'].append(val)
                self.annotations[i] = d
        with open('check111.json', 'w') as json_file:
            json.dump(self.annotations, json_file, indent=4)
        self.saved_label.config(text="Image data saved")

def main():
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
