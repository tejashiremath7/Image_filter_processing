import tkinter as tk
from tkinter import filedialog
from tkinter import font as tkFont
from PIL import Image, ImageFilter, ImageTk, ImageOps, ImageEnhance

def adjust_brightness(image, brightness_level):
    """
    Adjusts the brightness of an image.
    
    Args:
        image: The PIL image object to adjust.
        brightness_level: A float value representing the brightness adjustment.
            Positive values increase brightness, negative values decrease it.

    Returns:
        A new PIL image object with adjusted brightness.
    """
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(1 + brightness_level)

def apply_filter():
    """
    Applies filter, rotation, flip, scale, and brightness adjustments to the image.
    """
    img_path = image_entry.get()
    filter_type = filter_var.get()
    rotation_type = rotation_var.get()
    flip_type = flip_var.get()
    scale_type = scale_var.get()

    if not img_path:
        return

    image = Image.open(img_path)

    # Apply filter based on the selected option
    if filter_type == "Grayscale":
        filtered_image = image.convert("L")
    elif filter_type == "Sepia tone":
        sepia_image = image.convert("RGB")
        sepia_data = [
            (int(r*0.393 + g*0.769 + b*0.189),
             int(r*0.349 + g*0.686 + b*0.168),
             int(r*0.272 + g*0.534 + b*0.131))
            for r, g, b in sepia_image.getdata()
        ]
        sepia_image.putdata(sepia_data)
        filtered_image = sepia_image
    elif filter_type == "Edge detection":
        filtered_image = image.filter(ImageFilter.FIND_EDGES)
    else:
        filtered_image = image  # No filter applied

    # Apply rotation
    if rotation_type == "Rotate 90°":
        filtered_image = filtered_image.rotate(90, expand=True)
    elif rotation_type == "Rotate 180°":
        filtered_image = filtered_image.rotate(180, expand=True)

    # Apply flipping
    if flip_type == "Flip Horizontal":
        filtered_image = ImageOps.mirror(filtered_image)
    elif flip_type == "Flip Vertical":
        filtered_image = ImageOps.flip(filtered_image)

    # Apply scaling
    if scale_type == "Scale 50%":
        width, height = filtered_image.size
        filtered_image = filtered_image.resize((int(width * 0.5), int(height * 0.5)))

    # Apply brightness adjustment
    if brightness_var.get() != 0:
        filtered_image = adjust_brightness(filtered_image, float(brightness_var.get()))

    # Prompt user to select save location
    output_path = filedialog.asksaveasfilename(defaultextension=".png",
                                               filetypes=[("PNG files", "*.png"),
                                                          ("JPEG files", "*.jpg"),
                                                          ("All files", "*.*")])
    if output_path:
        # Save the output image
        filtered_image.save(output_path)

        # Update the output label with the preview of the output image
        output_image = Image.open(output_path)
        output_image.thumbnail((200, 200))
        output_photo = ImageTk.PhotoImage(output_image)
        output_label.configure(image=output_photo)
        output_label.image = output_photo

def browse_image():
    """
    Opens file browser to select image file.
    """
    img_path = filedialog.askopenfilename()
    image_entry.delete(0, tk.END)
    image_entry.insert(0, img_path)

# Create the main window
root = tk.Tk()
root.title("Image Filter")
root.geometry("400x600")

# Change the background color of the main window
root.configure(bg="#333333")

# Define a better font
font = tkFont.Font(family="Helvetica", size=12, weight="bold")

# Create a frame for the input section with a background color
input_frame = tk.Frame(root, padx=10, pady=10, bg="#444444")
input_frame.pack(pady=10, padx=10, fill="x")

# Create a frame for the control section with a background color
control_frame = tk.Frame(root, padx=10, pady=10, bg="#555555")
control_frame.pack(pady=10, padx=10, fill="x")

# Create a frame for the output section with a background color
output_frame = tk.Frame(root, padx=10, pady=10, bg="#444444")
output_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Create widgets in the input frame
image_entry = tk.Entry(input_frame, width=40, font=font)
browse_button = tk.Button(input_frame, text="Browse", command=browse_image, font=font)

# Place input widgets in the input frame
image_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
browse_button.grid(row=0, column=1, padx=10, pady=10)

# Create widgets in the control frame
filter_var = tk.StringVar(root)
filter_var.set("No Filter")  # default value
filter_menu = tk.OptionMenu(control_frame, filter_var, "No Filter", "Grayscale", "Sepia tone", "Edge detection")

rotation_var = tk.StringVar(root)
rotation_var.set("No Rotation")  # default value
rotation_menu = tk.OptionMenu(control_frame, rotation_var, "No Rotation", "Rotate 90°", "Rotate 180°")

flip_var = tk.StringVar(root)
flip_var.set("No Flip")  # default value
flip_menu = tk.OptionMenu(control_frame, flip_var, "No Flip", "Flip Horizontal", "Flip Vertical")

scale_var = tk.StringVar(root)
scale_var.set("No Scaling")  # default value
scale_menu = tk.OptionMenu(control_frame, scale_var, "No Scaling", "Scale 50%")

brightness_var = tk.DoubleVar(root)
brightness_scale = tk.Scale(control_frame, from_=-1.0, to=1.0, resolution=0.1, orient=tk.HORIZONTAL, label="Brightness", variable=brightness_var, bg="#555555", fg="#FFFFFF", font=font)

apply_button = tk.Button(control_frame, text="Apply", command=apply_filter, font=font)

# Place control widgets in the control frame
filter_menu.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
rotation_menu.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
flip_menu.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
scale_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
brightness_scale.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
apply_button.grid(row=3, column=0, columnspan=2, pady=10)

# Create and place the output label in the output frame
output_label = tk.Label(output_frame, text="Output image preview", width=200, height=200, font=font, bg="#333333", fg="#FFFFFF")
output_label.pack(pady=10, fill="both", expand=True)

# Start the main event loop
root.mainloop()
