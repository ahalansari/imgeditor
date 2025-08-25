#!/usr/bin/env python3
"""
Flask application for Qwen-Image-Edit integration - CUDA/RTX 3060 optimized version
"""

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
from werkzeug.utils import secure_filename
import uuid
from PIL import Image
import torch
from diffusers import QwenImageEditPipeline
import numpy as np

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Initialize the Qwen-Image-Edit pipeline
try:
    # Load the model - this might take some time on first run
    print("Loading Qwen-Image-Edit model...")
    model_id = "Qwen/Qwen-Image-Edit"
    
    # Optimized for RTX 3060 12GB
    if torch.cuda.is_available():
        device = "cuda"
        dtype = torch.float16  # Optimal for CUDA
        print(f"Using CUDA acceleration on {torch.cuda.get_device_name()}")
        print(f"VRAM Available: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")
    else:
        device = "cpu"
        dtype = torch.float32
        print("CUDA not available - using CPU (will be slower)")
    
    pipe = QwenImageEditPipeline.from_pretrained(
        model_id,
        torch_dtype=dtype,
        variant="fp16" if device == "cuda" else None  # Use fp16 variant for CUDA
    )
    pipe.to(device)
    
    # Memory optimizations for RTX 3060
    if device == "cuda":
        # Enable memory efficient attention
        pipe.enable_attention_slicing()
        
        # Optional: Enable CPU offload for very large images
        # Uncomment if you experience VRAM issues
        # pipe.enable_sequential_cpu_offload()
        
        # Clear CUDA cache
        torch.cuda.empty_cache()
    
    print(f"Model loaded successfully on {device} with {dtype}")
    
except Exception as e:
    print(f"Error loading model: {e}")
    # Fallback to a simpler approach if model loading fails
    pipe = None

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image_with_qwen(prompt, input_path, output_path):
    """
    Process image using Qwen-Image-Edit model with CUDA optimization
    """
    try:
        if pipe is None:
            print("Model not loaded, copying original image as fallback")
            # Fallback: copy original image
            img = Image.open(input_path)
            img.save(output_path)
            return False
        
        print(f"Processing image with prompt: '{prompt}'")
        
        # Load and preprocess image
        img = Image.open(input_path).convert("RGB")
        
        # Resize if too large for VRAM (RTX 3060 can handle larger images than MPS)
        max_size = 1536  # Increased for RTX 3060
        if max(img.size) > max_size:
            img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
            print(f"Resized image to {img.size} for processing")
        
        # Clear CUDA cache before processing
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Use Qwen-specific optimal parameters
        with torch.inference_mode():
            edited = pipe(
                image=img,
                prompt=prompt,
                true_cfg_scale=4.0,  # Qwen-specific parameter
                negative_prompt=" ",  # Required for better results
                num_inference_steps=50,  # Higher quality (RTX 3060 can handle this)
                generator=torch.manual_seed(0)  # Reproducible results
            ).images[0]
        
        # Clear CUDA cache after processing
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        # Save processed image
        edited.save(output_path, quality=95)
        print(f"Successfully processed and saved image to {output_path}")
        
        return True
        
    except Exception as e:
        print(f"Error processing image: {e}")
        
        # Clear CUDA cache on error
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            
        # Fallback: copy original image
        try:
            img = Image.open(input_path)
            img.save(output_path)
            print("Saved original image as fallback")
        except Exception as fallback_error:
            print(f"Fallback also failed: {fallback_error}")
        return False

@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/output/<filename>')
def output_file(filename):
    """Serve processed output files"""
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and image editing"""
    # Check if file was uploaded
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    # Check if prompt was provided
    if 'prompt' not in request.form or not request.form['prompt'].strip():
        flash('Please provide editing instructions', 'error')
        return redirect(url_for('index'))
    
    prompt = request.form['prompt'].strip()
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    # Validate and save file
    if file and allowed_file(file.filename):
        # Generate unique filename to avoid conflicts
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # Save uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Process the image with Qwen-Image-Edit
        output_filename = f"processed_{unique_filename}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Process the image
        success = process_image_with_qwen(prompt, file_path, output_path)
        
        return render_template('result.html',
                             original_image=unique_filename,
                             processed_image=output_filename if success else None)
    else:
        flash('Invalid file type. Please upload PNG, JPG, JPEG, or GIF files.', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
