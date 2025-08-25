# Technical Documentation - Qwen Image Editor Flask Application

## Overview
This Flask-based web application integrates the Qwen-Image-Edit model from Hugging Face to provide AI-powered image editing capabilities through a user-friendly web interface.

## Architecture

### Core Components

#### 1. Flask Web Application (`app.py`)
- **Framework**: Flask 2.3.3
- **Main functionality**: 
  - File upload handling with security validation
  - Image processing orchestration
  - Web UI serving
- **Configuration**:
  - Upload folder: `uploads/`
  - Output folder: `output/`
  - Max file size: 16MB
  - Supported formats: PNG, JPG, JPEG, GIF

#### 2. AI Model Integration
- **Model**: Qwen/Qwen-Image-Edit from Hugging Face
- **Framework**: Diffusers library with QwenImageEditPipeline
- **Device**: MPS (Metal Performance Shaders) for Mac M4 Max optimization
- **Precision**: float16 for memory efficiency on Apple Silicon

#### 3. Frontend Templates
- **Main page** (`templates/index.html`): Clean upload interface with drag-and-drop styling
- **Results page** (`templates/result.html`): Side-by-side comparison of original and processed images
- **Styling**: Modern CSS with responsive design, hover effects, and professional appearance

#### 4. Standalone Script (`script.py`)
- Direct CLI interface for testing Qwen-Image-Edit model
- Optimized for Mac M4 Max with MPS backend
- Minimal implementation for quick testing

### File Structure
```
imgeditor/
├── app.py                 # Flask web application
├── script.py             # Standalone testing script
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── input.jpg            # Sample input image
├── out.jpg             # Sample output image
├── templates/          # Jinja2 templates
│   ├── index.html      # Upload interface
│   └── result.html     # Results display
├── uploads/            # User uploaded images
├── output/             # Processed images
└── venv/              # Virtual environment
```

## Dependencies

### Core Requirements
```
Flask==2.3.3          # Web framework
Pillow==10.0.1         # Image processing
transformers           # Hugging Face transformers
torch                  # PyTorch ML framework
torchaudio            # Audio processing (dependency)
torchvision           # Computer vision utilities
```

### Additional Dependencies (Auto-installed)
- diffusers: For QwenImageEditPipeline
- safetensors: Model weight storage
- huggingface_hub: Model downloading and caching
- requests: HTTP utilities
- numpy: Numerical computing

## Technical Implementation Details

### Model Loading and Initialization
```python
# Optimized for Mac M4 Max
pipe = QwenImageEditPipeline.from_pretrained(
    "Qwen/Qwen-Image-Edit",
    torch_dtype=torch.float16,
    device_map="mps"
)
```

### Image Processing Pipeline
1. **Upload Validation**: File type and size checking
2. **Unique Naming**: UUID-based filename generation to prevent conflicts
3. **Model Processing**: Qwen-Image-Edit inference with configurable parameters
4. **Result Storage**: Processed images saved to output directory

### Security Features
- File extension validation
- Secure filename handling with `werkzeug.utils.secure_filename`
- File size limits (16MB)
- UUID-based naming to prevent directory traversal

## Performance Characteristics

### Mac M4 Max Optimization
- **MPS Backend**: Utilizes Apple's Metal Performance Shaders
- **Memory Efficiency**: float16 precision reduces VRAM usage
- **Model Caching**: Hugging Face automatic model caching
- **Inference Speed**: Optimized for Apple Silicon architecture

### Resource Requirements
- **RAM**: Minimum 16GB recommended for model loading
- **Storage**: ~20GB for model weights and cache
- **Compute**: Apple M4 Max optimized with MPS acceleration

## Current Capabilities

### Supported Operations
1. **Basic Image Upload**: PNG, JPG, JPEG, GIF formats
2. **AI-Powered Editing**: Using Qwen-Image-Edit model
3. **Web Interface**: User-friendly upload and result viewing
4. **Device Optimization**: Mac M4 Max MPS acceleration

### Model Features (Qwen-Image-Edit)
- **Semantic Editing**: High-level content modification while preserving semantics
- **Appearance Editing**: Precise pixel-level modifications
- **Text Editing**: Bilingual Chinese/English text manipulation
- **Style Transfer**: Artistic style transformations
- **Object Manipulation**: Adding, removing, or modifying elements

## Error Handling

### Current Implementation
- Model loading failure gracefully handled with fallback
- File validation with user feedback
- Flash message system for user notifications
- Exception catching in image processing pipeline

### Logging
- Basic print statements for debugging
- Model loading status messages
- Processing status indicators

## Configuration

### Environment Variables
- Currently using hardcoded configurations
- Secret key placeholder for production deployment

### Model Parameters
- Guidance scale: 7.5 (configurable)
- Inference steps: 8-50 (optimized for speed vs quality)
- Generator seed: Support for reproducible results

## Deployment Considerations

### Development Mode
- Debug mode enabled
- Host: 0.0.0.0 (accessible from network)
- Port: 5001 (configurable)

### Production Readiness
- Requires proper secret key configuration
- Need HTTPS for file uploads
- Consider model caching strategies
- Implement proper logging and monitoring

## Compatibility

### System Requirements
- **OS**: macOS with Apple Silicon (M1/M2/M3/M4)
- **Python**: 3.8+ (tested with 3.12)
- **PyTorch**: 2.7.1+ with MPS support
- **Memory**: 16GB+ RAM recommended

### Verified Compatibility
- ✅ Mac M4 Max with MPS acceleration
- ✅ PyTorch 2.7.1 with MPS backend
- ✅ Diffusers library with Qwen-Image-Edit pipeline
- ✅ Flask web serving on localhost
